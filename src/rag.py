"""Core RAG utilities using the OpenAI Responses API and vector stores."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o-mini")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

_client: Optional[OpenAI] = None


PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


class PromptNotFoundError(FileNotFoundError):
    """Raised when a prompt file for the requested use case does not exist."""


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def load_prompt(use_case: str) -> str:
    prompt_path = PROMPTS_DIR / f"{use_case}.md"
    if not prompt_path.exists():
        raise PromptNotFoundError(f"Prompt file not found for use case '{use_case}' at {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def generate_response(briefing: str, use_case: str, extra_context: Optional[str] = None) -> str:
    """Generate a response using the OpenAI Responses API with file_search."""
    if not VECTOR_STORE_ID:
        raise RuntimeError("VECTOR_STORE_ID environment variable is required.")

    client = get_client()
    system_prompt = load_prompt(use_case)

    user_sections = [f"Briefing do cliente:\n{briefing.strip()}"]
    if extra_context:
        user_sections.append(f"Contexto adicional fornecido:\n{extra_context.strip()}")
    user_prompt = "\n\n".join(user_sections)

    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
        ],
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [VECTOR_STORE_ID]}},
        temperature=0.2,
    )

    return response.output_text
