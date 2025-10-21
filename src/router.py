"""Simple keyword-based routing for client briefings."""
from __future__ import annotations

from typing import Dict, List, Tuple

import re

USE_CASE_KEYWORDS: Dict[str, List[str]] = {
    "analysis_guide": ["análise", "diagnóstico", "relatório", "guia", "apresentação"],
    "hypotheses": ["hipótese", "oportunidade", "growth", "crescimento", "ideia"],
    "validation_plan": ["validar", "validação", "teste", "experimento", "piloto"],
    "interview_questionnaire": ["entrevista", "questionário", "stakeholder", "pesquisa"],
}

USE_CASE_ORDER: Tuple[str, ...] = (
    "analysis_guide",
    "hypotheses",
    "validation_plan",
    "interview_questionnaire",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def detect_use_case(briefing: str) -> Tuple[str, List[str]]:
    """Return the selected use case and matched keywords."""
    normalized = normalize(briefing)

    for use_case in USE_CASE_ORDER:
        keywords = USE_CASE_KEYWORDS[use_case]
        hits = [kw for kw in keywords if kw in normalized]
        if hits:
            return use_case, hits
    return "analysis_guide", []


def route_briefing(briefing: str) -> Dict[str, object]:
    use_case, keywords = detect_use_case(briefing)
    return {
        "use_case": use_case,
        "matched_keywords": keywords,
    }
