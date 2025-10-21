"""Create a new OpenAI vector store for the Strategy On Demand project."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    client = OpenAI()

    name = os.getenv("VECTOR_STORE_NAME", "strategy-on-demand-store")
    vector_store = client.vector_stores.create(name=name)

    print("Vector Store criado com sucesso!")
    print(f"ID: {vector_store.id}")


if __name__ == "__main__":
    main()
