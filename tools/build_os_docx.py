#!/usr/bin/env python3
"""Generic DOCX materializer for `.osFactory` Especificações Funcionais / OS.

Converts the canonical OS Markdown (`05-output/<demanda>/OS-<demanda>.md`)
into a DOCX document, using `04-templates/docx/os-padrao.docx` as the
VISUAL source of truth (styles, page setup, header/footer) while the
Markdown remains the CONTENT source of truth.

This script is demand-agnostic by design: it never hardcodes a client
name, project code, or demand identifier. Everything it renders comes
from the Markdown file and the CLI arguments passed by the caller (the
`99-prompts/gerar-os.md` orchestrator, or a human operator).

Gate discipline (see os-rules.md, OS-QA-003):
  - FUNCTIONAL_BLOCKED is a content/specification problem and belongs to
    `os-validator-agent` / `validation.md`, evaluated BEFORE this script
    is ever invoked. This script does not re-judge functional quality.
  - OUTPUT_BLOCKED is a materialization failure (missing template,
    missing figure file, DOCX write error, etc.) and is the only kind of
    blocking condition this script can itself raise.
  - If `--validation-status BLOCKED` is passed explicitly, this script
    refuses to produce a DOCX and reports FUNCTIONAL_BLOCKED instead of
    silently generating a document that could be mistaken for an
    approved final OS.

Usage:
    python tools/build_os_docx.py \\
        --demand <demanda> \\
        --markdown 05-output/<demanda>/OS-<demanda>.md \\
        --template 04-templates/docx/os-padrao.docx \\
        --output 05-output/<demanda>/OS-<demanda>.docx
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

# --------------------------------------------------------------------------
# Exit / status vocabulary
# --------------------------------------------------------------------------

STATUS_OK = "OK"
STATUS_FUNCTIONAL_BLOCKED = "FUNCTIONAL_BLOCKED"
STATUS_OUTPUT_BLOCKED = "OUTPUT_BLOCKED"

EXIT_OK = 0
EXIT_FUNCTIONAL_BLOCKED = 3
EXIT_OUTPUT_BLOCKED = 2

USABLE_WIDTH_INCHES = 6.3  # A4 width (2.5cm+2.5cm margins) minus a small safety margin

MARKER_KEYWORDS = (
    "OPEN_QUESTION",
    "DISCOVERY_ITEM",
    "INFERENCE",
    "FUNCTIONAL_CONFLICT",
    "ARCHITECTURAL_CONFLICT",
    "DOCUMENTAL_CONFLICT",
    "CONFLICT_UNCLASSIFIED",
)
# Matches "[KEYWORD: ...]" or "[KEYWORD D1: ...]" (item ids like "D1"),
# with or without the surrounding brackets already stripped by the
# backtick/code-span tokenizer.
MARKER_PATTERN = re.compile(
    r"^\[?(" + "|".join(MARKER_KEYWORDS) + r")\b[^:]*:"
)

FIGURE_PATTERN = re.compile(
    r"^`?\[FIGURA:\s*(?P<description>.*?)\s*\|\s*fonte:\s*(?P<source>.*?)\]`?$"
)


class MaterializationError(Exception):
    """Raised for OUTPUT_BLOCKED conditions (materialization, not content)."""


class FunctionalGateError(Exception):
    """Raised when the caller explicitly signals a FUNCTIONAL_BLOCKED gate."""


# --------------------------------------------------------------------------
# Markdown parsing (structural, content-preserving — never rewrites text)
# --------------------------------------------------------------------------

@dataclass
class Block:
    kind: str  # heading | paragraph | bullet | table | figure | quote
    level: int = 0
    text: str = ""
    rows: List[List[str]] = field(default_factory=list)
    description: str = ""
    source: str = ""


def _split_table_row(line: str) -> List[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_table_separator(cells: List[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) is not None for c in cells if c.strip())


def parse_markdown(text: str) -> List[Block]:
    """Parse the OS Markdown into a flat list of structural blocks.

    Intentionally simple and line-oriented (see design note in the repo
    conversation / commit context): the `.osFactory` documenter agent
    produces one logical block per non-blank line, so no soft-wrap
    joining is required. This keeps the parser predictable and avoids
    any risk of silently merging or rewording adjacent sentences.
    """
    lines = text.splitlines()
    blocks: List[Block] = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # HTML comments (template instructions) — never materialized.
        if stripped.startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if m:
            blocks.append(Block(kind="heading", level=len(m.group(1)), text=m.group(2).strip()))
            i += 1
            continue

        # Figure marker (own line)
        fm = FIGURE_PATTERN.match(stripped)
        if fm:
            blocks.append(
                Block(
                    kind="figure",
                    description=fm.group("description").strip(),
                    source=fm.group("source").strip(),
                )
            )
            i += 1
            continue

        # Table block
        if stripped.startswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = [_split_table_row(l) for l in table_lines]
            if len(rows) >= 2 and _is_table_separator(rows[1]):
                rows = [rows[0]] + rows[2:]
            blocks.append(Block(kind="table", rows=rows))
            continue

        # Blockquote (exact system messages)
        if stripped.startswith(">"):
            blocks.append(Block(kind="quote", text=stripped.lstrip(">").strip()))
            i += 1
            continue

        # Bullet
        if stripped.startswith("- "):
            blocks.append(Block(kind="bullet", text=stripped[2:].strip()))
            i += 1
            continue

        # Plain paragraph (one line = one block, per the design note above)
        blocks.append(Block(kind="paragraph", text=stripped))
        i += 1

    return blocks


# --------------------------------------------------------------------------
# Inline formatting: bold (**...**) and code spans (`...`), incl. markers
# --------------------------------------------------------------------------

_INLINE_TOKEN = re.compile(r"(\*\*.+?\*\*|`.+?`)")


def iter_inline_runs(text: str):
    """Yield (text, is_bold, is_code) tuples for a line of inline markdown.

    Content is never altered — only classified for run formatting. Code
    spans are used verbatim for `[OPEN_QUESTION: ...]`,
    `[DISCOVERY_ITEM: ...]`, `[INFERENCE: ...]` and `CONFLICT` subtype
    markers, so they render distinctly without any special-casing beyond
    recognizing they are backtick-quoted, exactly like any other inline
    code span in the source Markdown.
    """
    for token in _INLINE_TOKEN.split(text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**") and len(token) >= 4:
            yield token[2:-2], True, False
        elif token.startswith("`") and token.endswith("`") and len(token) >= 2:
            yield token[1:-1], False, True
        else:
            yield token, False, False


def _is_marker_text(inner: str) -> bool:
    return bool(MARKER_PATTERN.match(inner.strip()))


# Direct run formatting (not named character styles) is used for code
# spans and markers, on purpose: it makes the generator work correctly
# against ANY conformant template, even one that does not define the
# optional "OS Marker"/"OS Code" character styles the official
# `os-padrao.docx` ships with. Named paragraph styles (Normal,
# Heading 1/2, List Bullet, Title, Caption) are still used, since those
# are virtually guaranteed to exist in any Word-compatible template.
_MARKER_COLOR = RGBColor(0x7A, 0x1F, 0x1F)
_CODE_COLOR = RGBColor(0x33, 0x33, 0x33)
_MONOSPACE_FONT = "Consolas"


# Monospace fonts commonly render visually larger than proportional body
# text at the same nominal point size (metrics differ, and font
# substitution on non-Windows renderers makes this worse). Code/marker
# runs are sized explicitly, slightly under body size, so they stay
# visually harmonious regardless of which monospace font is actually
# available on the rendering machine.
_CODE_SIZE = Pt(10)


def add_inline_runs(paragraph, text: str) -> None:
    for chunk, is_bold, is_code in iter_inline_runs(text):
        if not chunk:
            continue
        run = paragraph.add_run(chunk)
        if is_bold:
            run.bold = True
        if is_code:
            run.font.name = _MONOSPACE_FONT
            run.font.size = _CODE_SIZE
            if _is_marker_text(chunk):
                run.italic = True
                run.font.color.rgb = _MARKER_COLOR
            else:
                run.font.color.rgb = _CODE_COLOR


# --------------------------------------------------------------------------
# DOCX rendering
# --------------------------------------------------------------------------

HEADING_STYLE_BY_LEVEL = {1: "Title", 2: "Heading 1", 3: "Heading 2"}


def _clear_placeholder(doc: Document) -> None:
    """Remove the template's single placeholder paragraph, if present."""
    if not doc.paragraphs:
        return
    first = doc.paragraphs[0]
    if first.text.strip():
        # Only remove it when it looks like the known template placeholder
        # or is otherwise empty; never delete real content.
        if "template oficial" not in first.text.lower():
            return
    element = first._element
    element.getparent().remove(element)


def _render_table(doc: Document, rows: List[List[str]]) -> None:
    if not rows:
        return
    n_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.style = "Table Grid"
    for r_idx, row in enumerate(rows):
        for c_idx in range(n_cols):
            cell_text = row[c_idx] if c_idx < len(row) else ""
            cell = table.cell(r_idx, c_idx)
            cell.paragraphs[0].text = ""
            para = cell.paragraphs[0]
            add_inline_runs(para, cell_text)
            for run in para.runs:
                run.font.size = Pt(10)
            if r_idx == 0:
                for run in para.runs:
                    run.bold = True
    # blank line after table for breathing room
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)


def _resolve_figure(source: str, figures_dir: Optional[Path]) -> Path:
    if figures_dir is None:
        raise MaterializationError(
            f"figura referenciada ({source}) mas nenhum diretório de figuras foi informado"
        )
    candidate = figures_dir / source
    if not candidate.is_file():
        raise MaterializationError(
            f"figura ausente: esperado em {candidate} (referenciada como '{source}')"
        )
    return candidate


def _render_figure(doc: Document, block: Block, figures_dir: Optional[Path]) -> None:
    image_path = _resolve_figure(block.source, figures_dir)

    # Validate the file is actually a readable image before handing it to
    # python-docx (which would otherwise raise a less legible error).
    with Image.open(image_path) as img:
        img.verify()

    # Only width is set — python-docx preserves the image's native aspect
    # ratio automatically, so proportion is never distorted, and the
    # figure never exceeds the page's usable width.
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(str(image_path), width=Inches(USABLE_WIDTH_INCHES))

    caption = doc.add_paragraph(style="Caption")
    caption.text = f"Figura — {block.description} (fonte: {block.source})"


_FIXED_ZIP_DATETIME = (1980, 1, 1, 0, 0, 0)


def _normalize_zip_timestamps(docx_path: Path) -> None:
    """Rewrite every ZIP entry's timestamp to a fixed value.

    A .docx file is a ZIP container; python-docx (via the stdlib
    zipfile module) stamps each internal entry with the current
    wall-clock time on save. That alone would make two runs over the
    same Markdown/template produce different bytes even though the
    visible content is identical. Normalizing the timestamps makes the
    output byte-for-byte deterministic.
    """
    tmp_path = docx_path.with_suffix(docx_path.suffix + ".tmp")
    with zipfile.ZipFile(docx_path, "r") as src, zipfile.ZipFile(
        tmp_path, "w", zipfile.ZIP_DEFLATED
    ) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            item.date_time = _FIXED_ZIP_DATETIME
            dst.writestr(item, data)
    tmp_path.replace(docx_path)


def render_docx(
    blocks: List[Block],
    template_path: Path,
    output_path: Path,
    figures_dir: Optional[Path],
) -> None:
    if not template_path.is_file():
        raise MaterializationError(f"template DOCX não encontrado: {template_path}")

    # Work on a temp copy — the original template is never opened for
    # writing and is never modified.
    with tempfile.TemporaryDirectory() as tmp:
        working_copy = Path(tmp) / "working.docx"
        shutil.copyfile(template_path, working_copy)

        doc = Document(str(working_copy))
        _clear_placeholder(doc)

        for block in blocks:
            if block.kind == "heading":
                style = HEADING_STYLE_BY_LEVEL.get(block.level, "Heading 2")
                p = doc.add_paragraph(style=style)
                add_inline_runs(p, block.text)
            elif block.kind == "paragraph":
                p = doc.add_paragraph(style="Normal")
                add_inline_runs(p, block.text)
            elif block.kind == "bullet":
                p = doc.add_paragraph(style="List Bullet")
                add_inline_runs(p, block.text)
            elif block.kind == "quote":
                p = doc.add_paragraph(style="Intense Quote")
                add_inline_runs(p, block.text)
            elif block.kind == "table":
                _render_table(doc, block.rows)
            elif block.kind == "figure":
                _render_figure(doc, block, figures_dir)
            else:  # pragma: no cover - defensive
                raise MaterializationError(f"tipo de bloco desconhecido: {block.kind}")

        # Deterministic core properties: no wall-clock timestamps, so the
        # same Markdown + template always produce the same content.
        cp = doc.core_properties
        cp.author = ".osFactory"
        cp.last_modified_by = ".osFactory"
        cp.revision = 1

        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc.save(str(output_path))
            _normalize_zip_timestamps(output_path)
        except MaterializationError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            raise MaterializationError(f"falha ao salvar DOCX de saída: {exc}") from exc


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build(
    markdown_path: Path,
    template_path: Path,
    output_path: Path,
    figures_dir: Optional[Path],
    validation_status: Optional[str],
) -> None:
    if validation_status is not None and validation_status.upper() == "BLOCKED":
        raise FunctionalGateError(
            "validação funcional retornou BLOCKED — DOCX não pode ser gerado como "
            "documento final aprovado (ver os-rules.md, OS-QA-003). Corrija o "
            "conteúdo e revalide antes de materializar."
        )

    if not markdown_path.is_file():
        raise MaterializationError(f"Markdown de origem não encontrado: {markdown_path}")

    text = markdown_path.read_text(encoding="utf-8")
    blocks = parse_markdown(text)
    render_docx(blocks, template_path, output_path, figures_dir)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demand", required=True, help="Identificador da demanda (apenas para log/metadados)")
    parser.add_argument("--markdown", required=True, type=Path, help="Caminho do OS-<demanda>.md")
    parser.add_argument("--template", required=True, type=Path, help="Caminho do template DOCX oficial")
    parser.add_argument("--output", required=True, type=Path, help="Caminho do DOCX de saída")
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=None,
        help="Diretório onde localizar arquivos de figura referenciados por [FIGURA: ... | fonte: <arquivo>]. "
        "Padrão: 00-inbox/<demand>/ relativo à raiz do repositório (inferida a partir deste script).",
    )
    parser.add_argument(
        "--validation-status",
        default=None,
        choices=["PASS", "PASS_WITH_WARNINGS", "BLOCKED"],
        help="Resultado do os-validator-agent para esta demanda. Se BLOCKED, o script recusa gerar o DOCX.",
    )
    args = parser.parse_args(argv)

    figures_dir = args.figures_dir
    if figures_dir is None:
        repo_root = Path(__file__).resolve().parent.parent
        default_dir = repo_root / "00-inbox" / args.demand
        figures_dir = default_dir if default_dir.is_dir() else None

    try:
        build(
            markdown_path=args.markdown,
            template_path=args.template,
            output_path=args.output,
            figures_dir=figures_dir,
            validation_status=args.validation_status,
        )
    except FunctionalGateError as exc:
        print(f"{STATUS_FUNCTIONAL_BLOCKED}: {exc}")
        return EXIT_FUNCTIONAL_BLOCKED
    except MaterializationError as exc:
        print(f"{STATUS_OUTPUT_BLOCKED}: {exc}")
        return EXIT_OUTPUT_BLOCKED

    print(f"{STATUS_OK}: DOCX gerado em {args.output}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
