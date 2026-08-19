#!/usr/bin/env python3
"""Tests for tools/build_os_docx.py.

Uses a fully synthetic fixture (generic demand id, generic prose, a
generated placeholder PNG) — no real client, project or contract data.
Runs with the stdlib `unittest` runner so it has no extra dependency
beyond what `requirements.txt` already declares:

    python3 -m unittest tests.test_build_os_docx -v
    (run from the repository root)
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402
from PIL import Image  # noqa: E402

import build_os_docx as bod  # noqa: E402

# A markdown fixture that is deliberately generic: fictitious demand id,
# fictitious section content, no company/person/contract names.
FIXTURE_MARKDOWN = """# Documento de Especificação Funcional

## Identificação

- Código / Identificador da demanda: 0000-00-00-demo
- Nome da demanda: Demanda de exemplo genérica

## 1. DESCRIÇÃO

Texto de descrição genérico para fins de teste automatizado.

## 3. ESCOPO

`[FIGURA: Diagrama de exemplo | fonte: diagrama.png]`

### 3.1 Regras Funcionais

- Primeira regra de exemplo, com `identificador_tecnico` embutido.
- Segunda regra de exemplo. `[DISCOVERY_ITEM D1: item de exemplo — a descobrir na etapa de teste.]`

**Condição:** condição de exemplo.
**Comportamento esperado:** comportamento de exemplo. `[OPEN_QUESTION: pendência de exemplo?]`

`[ARCHITECTURAL_CONFLICT: divergência de exemplo entre duas fontes fictícias.]`

| Método / rota | Finalidade |
| --- | --- |
| `GET /api/v1/exemplo` | Endpoint de exemplo. |
| `GET /health` | Health check de exemplo. |

## 6. ESFORÇO

| Descrição | Esforço |
| --- | ---: |
| Total | 10 horas |
"""

FIXTURE_MARKDOWN_MISSING_FIGURE = FIXTURE_MARKDOWN.replace(
    "fonte: diagrama.png", "fonte: arquivo-que-nao-existe.png"
)

FORBIDDEN_SUBSTRINGS = [
    "SAGI",
    "GCONV",
    "Fundação PÁTRIA",
    "Thiago Mancilha",
    "Quanthum",
    "Entendimento Técnico",
]


def _build_minimal_template(path: Path) -> None:
    """Builds a tiny, fully generic DOCX template for test isolation.

    Deliberately independent from `04-templates/docx/os-padrao.docx` so
    these tests never depend on (or risk mutating) the real official
    template, and stay fast/self-contained.
    """
    doc = Document()
    for name in ("Normal", "Title", "Heading 1", "Heading 2", "List Bullet", "Caption"):
        style = doc.styles[name]
        style.font.size = Pt(11 if name in ("Normal", "List Bullet") else 13)
    placeholder = doc.add_paragraph("[template oficial de teste]")
    doc.save(str(path))


class BuildOsDocxTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="osfactory_test_"))
        self.template_path = self.tmp / "template.docx"
        _build_minimal_template(self.template_path)

        self.figures_dir = self.tmp / "00-inbox" / "0000-00-00-demo"
        self.figures_dir.mkdir(parents=True)
        img = Image.new("RGB", (800, 400), color=(210, 210, 210))
        img.save(self.figures_dir / "diagrama.png")

        self.markdown_path = self.tmp / "OS-0000-00-00-demo.md"
        self.markdown_path.write_text(FIXTURE_MARKDOWN, encoding="utf-8")

        self.output_path = self.tmp / "out" / "OS-0000-00-00-demo.docx"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _build(self, markdown_path=None):
        bod.build(
            markdown_path=markdown_path or self.markdown_path,
            template_path=self.template_path,
            output_path=self.output_path,
            figures_dir=self.figures_dir,
            validation_status=None,
        )

    # 1. template original não é modificado
    def test_template_not_modified(self):
        before = self.template_path.read_bytes()
        self._build()
        after = self.template_path.read_bytes()
        self.assertEqual(before, after)

    # 2. DOCX é criado
    def test_docx_is_created(self):
        self._build()
        self.assertTrue(self.output_path.is_file())

    # 3. headings são materializados
    def test_headings_materialized(self):
        self._build()
        doc = Document(str(self.output_path))
        styles_seen = {p.style.name for p in doc.paragraphs}
        self.assertIn("Title", styles_seen)
        self.assertIn("Heading 1", styles_seen)
        self.assertIn("Heading 2", styles_seen)

    # 4. texto essencial aparece
    def test_essential_text_present(self):
        self._build()
        doc = Document(str(self.output_path))
        full_text = "\n".join(p.text for p in doc.paragraphs)
        self.assertIn("Texto de descrição genérico para fins de teste automatizado.", full_text)

    # 5. bullets funcionam
    def test_bullets_render(self):
        self._build()
        doc = Document(str(self.output_path))
        bullets = [p.text for p in doc.paragraphs if p.style.name == "List Bullet"]
        self.assertTrue(any("Primeira regra de exemplo" in b for b in bullets))

    # 6. tabela funciona
    def test_table_renders(self):
        self._build()
        doc = Document(str(self.output_path))
        self.assertEqual(len(doc.tables), 2)
        endpoints_table = doc.tables[0]
        self.assertEqual(endpoints_table.cell(0, 0).text, "Método / rota")
        self.assertEqual(endpoints_table.cell(1, 0).text, "GET /api/v1/exemplo")

    # 7. subseções dinâmicas funcionam
    def test_dynamic_subsection_renders(self):
        self._build()
        doc = Document(str(self.output_path))
        h2_texts = [p.text for p in doc.paragraphs if p.style.name == "Heading 2"]
        self.assertIn("3.1 Regras Funcionais", h2_texts)

    # 8. figura válida é inserida
    def test_valid_figure_inserted(self):
        self._build()
        doc = Document(str(self.output_path))
        self.assertEqual(len(doc.inline_shapes), 1)
        captions = [p.text for p in doc.paragraphs if p.style.name == "Caption"]
        self.assertTrue(any("Diagrama de exemplo" in c for c in captions))

    # 9. figura inexistente gera erro controlado
    def test_missing_figure_raises_materialization_error(self):
        bad_markdown = self.tmp / "OS-bad.md"
        bad_markdown.write_text(FIXTURE_MARKDOWN_MISSING_FIGURE, encoding="utf-8")
        with self.assertRaises(bod.MaterializationError):
            self._build(markdown_path=bad_markdown)
        self.assertFalse(self.output_path.exists())

    # 10. marcadores de incerteza/conflito são preservados
    def test_uncertainty_and_conflict_markers_preserved(self):
        self._build()
        doc = Document(str(self.output_path))
        full_text = "\n".join(p.text for p in doc.paragraphs)
        self.assertIn("[DISCOVERY_ITEM D1: item de exemplo — a descobrir na etapa de teste.]", full_text)
        self.assertIn("[OPEN_QUESTION: pendência de exemplo?]", full_text)
        self.assertIn("[ARCHITECTURAL_CONFLICT: divergência de exemplo entre duas fontes fictícias.]", full_text)
        marker_runs = [
            r.text
            for p in doc.paragraphs
            for r in p.runs
            if r.italic and r.font.name == "Consolas"
        ]
        self.assertTrue(any("DISCOVERY_ITEM" in m for m in marker_runs))

    # 11. nenhum nome de cliente está hardcoded
    def test_no_hardcoded_client_names_in_tool_source(self):
        source = (REPO_ROOT / "tools" / "build_os_docx.py").read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_SUBSTRINGS:
            self.assertNotIn(forbidden, source)

    # Functional gate: BLOCKED must never produce a DOCX.
    def test_functional_blocked_refuses_to_build(self):
        with self.assertRaises(bod.FunctionalGateError):
            bod.build(
                markdown_path=self.markdown_path,
                template_path=self.template_path,
                output_path=self.output_path,
                figures_dir=self.figures_dir,
                validation_status="BLOCKED",
            )
        self.assertFalse(self.output_path.exists())

    # Determinism: same inputs -> byte-identical output.
    def test_deterministic_output(self):
        self._build()
        first = self.output_path.read_bytes()
        second_output = self.tmp / "out2" / "OS-0000-00-00-demo.docx"
        bod.build(
            markdown_path=self.markdown_path,
            template_path=self.template_path,
            output_path=second_output,
            figures_dir=self.figures_dir,
            validation_status=None,
        )
        second = second_output.read_bytes()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
