# Strategy On Demand – RAG MVP

MVP em FastAPI para geração de entregáveis estratégicos usando **OpenAI Responses API** com `file_search` conectado a Vector Stores.

## Estrutura principal
- `src/app.py` – API FastAPI com os endpoints `/briefing-router` e `/generate`.
- `src/router.py` – Heurística baseada em palavras-chave para classificar briefings.
- `src/rag.py` – Integração com a OpenAI Responses API (`gpt-4o-mini`) e Vector Store.
- `src/prompts/*.md` – Prompts específicos por use case, já no formato de resposta esperado.
- `scripts/create_vector_store.py` – Cria um Vector Store e imprime o ID.
- `scripts/upload_files.py` – Faz upload dos arquivos em `data/input/` para o Vector Store configurado.
- `data/input/` – Exemplos de arquivos dummy para testes.

## Pré-requisitos
1. Crie um `.env` baseado em `.env.example` com `OPENAI_API_KEY`, `MODEL` (opcional), `VECTOR_STORE_ID` e `PORT` (para Docker/Render).
2. O projeto depende de Python 3.11+.

## Criar o Vector Store
```bash
python scripts/create_vector_store.py
```
O script imprime o ID que deve ser salvo em `.env` na variável `VECTOR_STORE_ID`.

## Fazer upload dos arquivos de referência
```bash
python scripts/upload_files.py
```
Os arquivos em `data/input/` serão enviados ao Vector Store informado no `.env`.

## Deploy no Render
1. Faça o push do repositório para o GitHub.
2. Crie um novo serviço **Web Service** no Render com o repositório.
3. Render detectará o `render.yaml` e configurará o deploy via Docker.
4. Defina as variáveis de ambiente sensíveis (`OPENAI_API_KEY`, `VECTOR_STORE_ID`) diretamente no Render.

O container expõe a aplicação via `gunicorn` + `uvicorn` na porta configurada por `PORT` (padrão `8000`).
