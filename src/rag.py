"""Core RAG utilities using the OpenAI Responses API and vector stores."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
_client: Optional[OpenAI] = None


class PromptNotFoundError(FileNotFoundError):
    """Raised when a prompt file for the requested use case does not exist."""


def get_client() -> OpenAI:
    """Return a singleton OpenAI client instance."""
    global _client
    if _client is None:
        # usa a chave do ambiente se estiver definida
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def load_prompt(use_case: str) -> str:
    """Load the markdown prompt template associated with the use case."""
    prompt_path = PROMPTS_DIR / f"{use_case}.md"
    if not prompt_path.exists():
        raise PromptNotFoundError(
            f"Prompt file not found for use case '{use_case}' at {prompt_path}"
        )
    return prompt_path.read_text(encoding="utf-8")


def build_prompt(*, use_case: str, briefing: str, extra_context: Optional[str] = None) -> str:
    """Compose the full prompt combining template, briefing, and optional context."""
    template = load_prompt(use_case).strip()
    sections = [template, f"Briefing do cliente:\n{briefing.strip()}"]
    if extra_context:
        sections.append(f"Contexto adicional fornecido:\n{extra_context.strip()}")
    return "\n\n".join(section for section in sections if section)


def generate_response(
    *,
    briefing: str,
    use_case: str,
    extra_context: Optional[str] = None,
    vector_store_id: Optional[str] = None,
    k: int = 12,
) -> str:
    """Generate a response using the OpenAI Responses API with file_search."""
    resolved_vector_store = vector_store_id or os.getenv("VECTOR_STORE_ID")
    if not resolved_vector_store:
        raise RuntimeError("VECTOR_STORE_ID environment variable is required.")

    client = get_client()
    model = os.getenv("MODEL", "gpt-5-thinking")
    temperature = float(os.getenv("TEMPERATURE", "0.1"))
    full_prompt = build_prompt(
        use_case=use_case, briefing=briefing, extra_context=extra_context
    )

    response = client.responses.create(
        model=model,
        temperature=temperature,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [resolved_vector_store],
            "max_num_results": k,
        }],
        input=[{
            "role": "user",
            "content": [{"type": "input_text", "text": full_prompt}],
        }],
    )

    # Prefer the convenience accessor; fallback to manual concat if absent
    try:
        return response.output_text.strip()
    except AttributeError:
        parts: list[str] = []
        for item in getattr(response, "output", []) or []:
            if getattr(item, "type", "") == "message":
                for content in getattr(item, "content", []) or []:
                    if content.get("type") == "text":
                        parts.append(content.get("text", ""))
        return "\n".join(p for p in parts if p).strip()
