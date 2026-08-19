#!/usr/bin/env python3
"""Commercial-condition resolution and persistence for `.osFactory` OS.

Implements the authority hierarchy for Horas contratadas / Valor total da
OS / Forma de pagamento (see os-rules.md, OS-COMMERCIAL-001):

    1. explicitly confirmed by the user for THIS run (CLI flags on
       tools/build_os_docx.py);
    2. a specific, valid condition already present in the OS Markdown
       (an insumo, authored by os-documenter-agent from 00-inbox/);
    3. a condition already registered for this OS from a PRIOR explicit
       confirmation (persisted, local, git-ignored registry);
    4. Tria's standard commercial policy
       (config/os-commercial-policy.json) — applied only when nothing
       above is available, and only for Forma de pagamento (Horas and
       Valor have no factory-wide default; they must come from real
       information).

A tier-1 confirmation is persisted into the registry so it becomes the
tier-3 "already registered" answer for future regenerations of the same
demand, without requiring the CLI flags to be repeated every time.

This module contains NO functional content and NO client data beyond
whatever the caller explicitly persists for a given demand id.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_COMMERCIAL_REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "01-analysis" / "_runtime" / "os-commercial.json"
)
DEFAULT_POLICY_PATH = Path(__file__).resolve().parent.parent / "config" / "os-commercial-policy.json"

PAYMENT_BY_MILESTONES_RECOMMENDED = "PAYMENT_BY_MILESTONES_RECOMMENDED"


class CommercialError(Exception):
    """Raised for malformed explicit input (bad currency, splits != 100%)."""


# --------------------------------------------------------------------------
# Registry (persisted, git-ignored — see .gitignore, /01-analysis/*)
# --------------------------------------------------------------------------

def load_commercial_registry(path: Optional[Path] = None) -> Dict:
    path = path or DEFAULT_COMMERCIAL_REGISTRY_PATH
    if not path.is_file():
        return {"demands": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("demands", {})
    return data


def save_commercial_registry(data: Dict, path: Optional[Path] = None) -> None:
    path = path or DEFAULT_COMMERCIAL_REGISTRY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(path)


# --------------------------------------------------------------------------
# Institutional policy (versioned)
# --------------------------------------------------------------------------

def load_policy(path: Optional[Path] = None) -> Dict:
    path = path or DEFAULT_POLICY_PATH
    if not path.is_file():
        raise CommercialError(f"política comercial não encontrada: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("limite_horas_pagamento_padrao", "parcelas_padrao"):
        if key not in data:
            raise CommercialError(f"config/os-commercial-policy.json incompleto — faltando: {key}")
    return data


# --------------------------------------------------------------------------
# BRL / hours parsing and formatting
# --------------------------------------------------------------------------

def parse_brl(value: str) -> Decimal:
    cleaned = value.replace("R$", "").strip()
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return Decimal(cleaned)
    except Exception as exc:  # pragma: no cover - defensive
        raise CommercialError(f"valor monetário inválido: {value!r}") from exc


def format_brl(value: Decimal) -> str:
    value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = f"{value:,.2f}"
    s = s.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {s}"


def parse_hours(value: Optional[str]) -> Optional[Decimal]:
    if not value:
        return None
    m = re.search(r"(\d+(?:[.,]\d+)?)", value)
    if not m:
        return None
    return Decimal(m.group(1).replace(",", "."))


# --------------------------------------------------------------------------
# Installments (marcos de pagamento)
# --------------------------------------------------------------------------

def compute_installments(total_value: str, splits: List[Dict]) -> List[Dict]:
    """`splits`: [{"marco": str, "percentual": number}, ...], summing to 100.

    Returns [{"marco":..., "percentual":..., "valor": "R$ ..."}]. The sum
    of `valor` always reconciles EXACTLY to `total_value` — the last
    installment absorbs any rounding remainder, so parcels never drift
    from the total by a cent.
    """
    if not splits:
        raise CommercialError("nenhum marco de pagamento informado")
    total_pct = sum(Decimal(str(s["percentual"])) for s in splits)
    if total_pct != Decimal("100"):
        raise CommercialError(f"percentuais somam {total_pct}, esperado 100")

    total = parse_brl(total_value)
    result = []
    allocated = Decimal("0")
    for i, s in enumerate(splits):
        if i == len(splits) - 1:
            amount = total - allocated
        else:
            amount = (total * Decimal(str(s["percentual"])) / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            allocated += amount
        result.append({"marco": s["marco"], "percentual": s["percentual"], "valor": format_brl(amount)})
    return result


def format_forma_pagamento(installments: List[Dict]) -> str:
    return "; ".join(f"{i['percentual']}% {i['marco']} — {i['valor']}" for i in installments)


# --------------------------------------------------------------------------
# Field-level resolution (see module docstring for the 4-tier hierarchy)
# --------------------------------------------------------------------------

def _is_absent(value: Optional[str]) -> bool:
    if value is None:
        return True
    stripped = value.strip()
    return (not stripped) or ("OPEN_QUESTION" in stripped)


@dataclass
class ResolvedField:
    value: Optional[str]
    source: str  # "usuario_confirmado" | "insumos" | "registry" | "politica_padrao_tria" | "ausente" | PAYMENT_BY_MILESTONES_RECOMMENDED


def resolve_commercial_terms(
    *,
    demand: str,
    explicit_horas: Optional[str],
    explicit_valor: Optional[str],
    explicit_pagamento_splits: Optional[List[Dict]],
    explicit_note: Optional[str],
    insumos: Dict[str, str],
    policy: Dict,
    registry_path: Optional[Path] = None,
) -> Dict[str, ResolvedField]:
    registry = load_commercial_registry(registry_path)
    registered = registry["demands"].get(demand, {})

    # --- Horas contratadas -------------------------------------------------
    if explicit_horas:
        horas = ResolvedField(explicit_horas, "usuario_confirmado")
    elif not _is_absent(insumos.get("horas contratadas")):
        horas = ResolvedField(insumos["horas contratadas"], "insumos")
    elif registered.get("horas_contratadas"):
        horas = ResolvedField(registered["horas_contratadas"], "registry")
    else:
        horas = ResolvedField(None, "ausente")

    # --- Valor total da OS ---------------------------------------------------
    if explicit_valor:
        valor = ResolvedField(explicit_valor, "usuario_confirmado")
    elif not _is_absent(insumos.get("valor total da os")):
        valor = ResolvedField(insumos["valor total da os"], "insumos")
    elif registered.get("valor_total_os"):
        valor = ResolvedField(registered["valor_total_os"], "registry")
    else:
        valor = ResolvedField(None, "ausente")

    # --- Forma / condição de pagamento -----------------------------------
    forma_key = "forma/condição de pagamento"
    multi_phase_signal = insumos.get("fases relevantes de execução")
    multi_phase = bool(multi_phase_signal) and multi_phase_signal.strip().lower() not in ("", "não", "nao", "n/a")

    if explicit_pagamento_splits:
        if valor.value:
            installments = compute_installments(valor.value, explicit_pagamento_splits)
            pagamento = ResolvedField(format_forma_pagamento(installments), "usuario_confirmado")
        else:
            # A payment split was explicitly confirmed but the total value is
            # still unknown: the schedule is real (user-confirmed) but not yet
            # a concrete, reconciled amount, so it must not count as a fully
            # resolved commercial condition for acceptance-readiness purposes.
            pagamento = ResolvedField(
                "[OPEN_QUESTION: valor total da OS ainda não confirmado; "
                "distribuição de pagamento informada (" +
                "; ".join(f"{s['percentual']}% {s['marco']}" for s in explicit_pagamento_splits) +
                ") não pode ser expressa em valores até que o valor total seja definido.]",
                "ausente",
            )
    elif not _is_absent(insumos.get(forma_key)):
        pagamento = ResolvedField(insumos[forma_key], "insumos")
    elif registered.get("forma_pagamento"):
        pagamento = ResolvedField(registered["forma_pagamento"], "registry")
    else:
        horas_num = parse_hours(horas.value)
        over_limit = horas_num is not None and horas_num > Decimal(str(policy["limite_horas_pagamento_padrao"]))
        unknown_effort = horas_num is None
        if multi_phase or over_limit:
            pagamento = ResolvedField(
                "[OPEN_QUESTION: definir a distribuição do pagamento entre os marcos da Ordem de Serviço "
                "(marcos sugeridos de referência em config/os-commercial-policy.json: "
                + ", ".join(policy.get("marcos_sugeridos_referencia", [])) + ").]",
                PAYMENT_BY_MILESTONES_RECOMMENDED,
            )
        elif unknown_effort:
            # Cannot safely default without knowing effort (could turn out >80h).
            pagamento = ResolvedField(None, "ausente")
        else:
            if valor.value:
                installments = compute_installments(valor.value, policy["parcelas_padrao"])
                pagamento = ResolvedField(format_forma_pagamento(installments), "politica_padrao_tria")
            else:
                # Policy default (50/50) applies by structure, but without a
                # known total value there is no concrete, reconciled amount
                # to show yet — must count as still-missing for readiness.
                pagamento = ResolvedField(None, "ausente")

    # Persist any fresh tier-1 confirmation so future regenerations read it
    # back as tier-3 ("já registrada"), without needing the CLI flags again.
    if explicit_horas or explicit_valor or explicit_pagamento_splits:
        registry["demands"][demand] = {
            "horas_contratadas": horas.value,
            "valor_total_os": valor.value,
            "forma_pagamento": pagamento.value if pagamento.source == "usuario_confirmado" else registered.get("forma_pagamento"),
            "nota": explicit_note,
        }
        save_commercial_registry(registry, registry_path)

    return {"horas contratadas": horas, "valor total da os": valor, "forma/condição de pagamento": pagamento}
