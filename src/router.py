"""Simple keyword-based routing for client briefings."""
from __future__ import annotations

from typing import Dict, List, Tuple

import re

USE_CASE_KEYWORDS: Dict[str, List[str]] = {
    # Expanded with English terms and common variants for better matching
    "analysis_guide": [
        # PT
        "análise", "analise", "diagnóstico", "diagnostico", "diagnosticar",
        "relatório", "relatorio", "guia", "apresentação", "apresentacao",
        "modelo", "estrutura", "distribuidor", "distribuidores", "canal",
        "rtm", "roteiro", "plano", "transformação", "transformacao",
        # EN
        "analysis", "diagnosis", "diagnose", "report", "guide", "presentation",
        "model", "structure", "distributor", "distributors", "channel",
        "rtm structure", "route to market", "rtm transformation",
    ],
    "hypotheses": [
        # PT
        "hipótese", "hipoteses", "hipótese", "hipóteses", "oportunidade",
        "growth", "crescimento", "ideia", "alavanca", "driver",
        # EN
        "hypothesis", "hypotheses", "opportunity", "opportunities", "idea",
        "growth driver", "growth", "lever", "driver",
    ],
    "validation_plan": [
        # PT
        "validar", "validação", "validacao", "teste", "experimento", "piloto",
        "prova", "cobertura", "coverage", "plano de validação", "plano de validacao",
        "pilot test",
        # EN
        "validate", "validation", "test", "testing", "experiment", "pilot",
        "pilot test", "coverage", "rollout",
    ],
    "interview_questionnaire": [
        # PT
        "entrevista", "questionário", "questionario", "stakeholder", "pesquisa",
        "roteiro de entrevista", "guia de entrevista",
        # EN
        "interview", "questionnaire", "stakeholder", "survey", "interview guide",
    ],
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
