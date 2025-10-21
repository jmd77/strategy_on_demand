"""Upload local data/input files to the configured OpenAI vector store."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm


DATA_DIR = Path("data/input")


def main() -> None:
    load_dotenv()
    vector_store_id = os.getenv("VECTOR_STORE_ID")
    if not vector_store_id:
        raise RuntimeError("Defina VECTOR_STORE_ID no arquivo .env antes de fazer o upload.")

    client = OpenAI()

    files = [path for path in DATA_DIR.iterdir() if path.is_file()]
    if not files:
        raise RuntimeError(f"Nenhum arquivo encontrado em {DATA_DIR}.")

    print(f"Enviando {len(files)} arquivo(s) para o Vector Store {vector_store_id}...")
    for path in tqdm(files, desc="Upload"):
        with path.open("rb") as file_handle:
            uploaded_file = client.files.create(file=file_handle, purpose="assistants")
        client.vector_stores.files.create(vector_store_id=vector_store_id, file_id=uploaded_file.id)
        print(f"✔ Arquivo '{path.name}' anexado (file_id={uploaded_file.id})")

    print("Upload concluído!")


if __name__ == "__main__":
    main()
