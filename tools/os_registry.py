#!/usr/bin/env python3
"""OS code registry for `.osFactory` (see os-rules.md, OS-CODE-001).

Assigns and persists the traceable code (`OS-<AAAA>-<NNNN>`) for each
demand, in a LOCAL, git-ignored registry file
(`01-analysis/_runtime/os-registry.json` by default — already covered by
the existing `/01-analysis/*` ignore rule).

This module contains NO functional content and NO client data: only the
mapping `demanda -> código` and a per-year sequential counter.

Authority order for resolving a demand's code (never reuse a code
already assigned to a *different* demand):
  1. an explicitly informed/confirmed code (`explicit_code`);
  2. the code already recorded in the registry for this demand;
  3. automatic generation of the next sequential code for the year.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

CODE_PATTERN = re.compile(r"^OS-(\d{4})-(\d{4})$")

DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "01-analysis" / "_runtime" / "os-registry.json"
)


class RegistryError(Exception):
    """Raised for invalid code formats or code-reuse conflicts."""


def _empty_registry() -> dict:
    return {"demands": {}, "years": {}}


def load_registry(path: Optional[Path] = None) -> dict:
    path = path or DEFAULT_REGISTRY_PATH
    if not path.is_file():
        return _empty_registry()
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("demands", {})
    data.setdefault("years", {})
    return data


def save_registry(data: dict, path: Optional[Path] = None) -> None:
    path = path or DEFAULT_REGISTRY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    tmp_path.replace(path)


def validate_code_format(code: str) -> None:
    if not CODE_PATTERN.match(code):
        raise RegistryError(f"código '{code}' não segue o formato OS-AAAA-NNNN")


def resolve_os_code(
    demand: str,
    year: str,
    explicit_code: Optional[str] = None,
    registry_path: Optional[Path] = None,
) -> str:
    """Resolve the OS code for `demand`, persisting the assignment.

    `year` is only used when a NEW code must be auto-generated (case 3);
    it is ignored when an explicit code is given or a code already
    exists for this demand in the registry.
    """
    path = registry_path or DEFAULT_REGISTRY_PATH
    data = load_registry(path)
    demands = data["demands"]
    years = data["years"]

    if explicit_code:
        validate_code_format(explicit_code)
        for other_demand, other_code in demands.items():
            if other_code == explicit_code and other_demand != demand:
                raise RegistryError(
                    f"código {explicit_code} já está atribuído à demanda "
                    f"'{other_demand}' — não pode ser reatribuído a '{demand}'"
                )
        demands[demand] = explicit_code
        code_year, code_seq = CODE_PATTERN.match(explicit_code).groups()
        years[code_year] = max(years.get(code_year, 0), int(code_seq))
        save_registry(data, path)
        return explicit_code

    if demand in demands:
        return demands[demand]

    next_seq = years.get(year, 0) + 1
    code = f"OS-{year}-{next_seq:04d}"
    years[year] = next_seq
    demands[demand] = code
    save_registry(data, path)
    return code


def peek_os_code(demand: str, registry_path: Optional[Path] = None) -> Optional[str]:
    """Return the demand's already-assigned code without allocating a new one."""
    data = load_registry(registry_path or DEFAULT_REGISTRY_PATH)
    return data["demands"].get(demand)
