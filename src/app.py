"""FastAPI application exposing briefing routing and generation endpoints."""
from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import rag, router

load_dotenv()

USE_CASES = {
    "analysis_guide",
    "hypotheses",
    "validation_plan",
    "interview_questionnaire",
}

app = FastAPI(title="Strategy On Demand RAG MVP")


class BriefingRequest(BaseModel):
    briefing: str = Field(..., description="Briefing textual fornecido pelo cliente.")


class GenerateRequest(BaseModel):
    briefing: str = Field(..., description="Briefing textual fornecido pelo cliente.")
    use_case: Optional[str] = Field(None, description="Use case desejado. Se não informado, será roteado automaticamente.")
    extra_context: Optional[str] = Field(None, description="Informações adicionais a serem consideradas na geração.")


class GenerateResponse(BaseModel):
    use_case: str
    matched_keywords: List[str]
    content: str


@app.post("/briefing-router")
def briefing_router(payload: BriefingRequest) -> dict:
    """Classify the incoming briefing into a supported use case."""
    result = router.route_briefing(payload.briefing)
    return result


@app.post("/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest) -> GenerateResponse:
    """Generate content for the given briefing leveraging the RAG pipeline."""
    use_case = payload.use_case
    matched_keywords: List[str] = []

    if use_case:
        if use_case not in USE_CASES:
            raise HTTPException(status_code=400, detail=f"Use case '{use_case}' não suportado.")
    else:
        routing = router.route_briefing(payload.briefing)
        use_case = routing["use_case"]
        matched_keywords = routing.get("matched_keywords", [])

    try:
        content = rag.generate_response(
            briefing=payload.briefing,
            use_case=use_case,
            extra_context=payload.extra_context,
        )
    except rag.PromptNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - safety net for runtime errors
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resposta: {exc}") from exc

    if not matched_keywords and use_case:
        matched_keywords = router.route_briefing(payload.briefing).get("matched_keywords", [])

    return GenerateResponse(
        use_case=use_case,
        matched_keywords=matched_keywords,
        content=content,
    )


@app.get("/")
def read_root() -> dict:
    return {
        "message": "Strategy On Demand RAG MVP ativo.",
        "model": os.getenv("MODEL", "gpt-4o-mini"),
    }
