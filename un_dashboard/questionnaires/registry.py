"""Questionnaire registry with dynamic package discovery."""

from __future__ import annotations

import importlib
import pkgutil
import re
from pathlib import Path
from typing import Dict, List

from un_dashboard.questionnaires.base import QuestionnaireSchema

_DEFAULT_KEY = "gwo_beneficiaries"


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")


def _discover_questionnaires() -> Dict[str, QuestionnaireSchema]:
    out: Dict[str, QuestionnaireSchema] = {}
    package_dir = Path(__file__).parent
    for mod in pkgutil.iter_modules([str(package_dir)]):
        if not mod.ispkg or mod.name.startswith("_"):
            continue
        try:
            schema_mod = importlib.import_module(f"un_dashboard.questionnaires.{mod.name}.schema")
            schema_obj = getattr(schema_mod, "SCHEMA", None)
            if isinstance(schema_obj, QuestionnaireSchema):
                out[schema_obj.key] = schema_obj
        except Exception:
            continue
    return out


QUESTIONNAIRES: Dict[str, QuestionnaireSchema] = _discover_questionnaires()


def list_questionnaires() -> List[QuestionnaireSchema]:
    return [QUESTIONNAIRES[k] for k in sorted(QUESTIONNAIRES.keys())]


def get_questionnaire(key: str) -> QuestionnaireSchema:
    if key in QUESTIONNAIRES:
        return QUESTIONNAIRES[key]
    if _DEFAULT_KEY in QUESTIONNAIRES:
        return QUESTIONNAIRES[_DEFAULT_KEY]
    if QUESTIONNAIRES:
        return next(iter(QUESTIONNAIRES.values()))
    raise RuntimeError("No questionnaire schema registered.")


def questionnaire_key_for_sheet_name(sheet_name: str) -> str:
    return _normalize_key(sheet_name)


def get_questionnaire_for_sheet_name(sheet_name: str) -> QuestionnaireSchema | None:
    return QUESTIONNAIRES.get(questionnaire_key_for_sheet_name(sheet_name))
