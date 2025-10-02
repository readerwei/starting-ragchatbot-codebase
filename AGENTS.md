# Repository Guidelines

## Project Structure & Module Organization
The FastAPI backend lives in `backend/`, with `app.py` exposing HTTP routes, `rag_system.py` orchestrating retrieval and generation, and helpers such as `vector_store.py`, `search_tools.py`, and `session_manager.py`. Configuration defaults stay in `backend/config.py`. Persistent embeddings land in the root `chroma_db/` folder; treat it as generated data and exclude it from pull requests. Course source material belongs under `docs/`, while the static client (`index.html`, `script.js`, `style.css`) resides in `frontend/`. Backend tests and fixtures sit in `backend/tests/` alongside the code they cover.

## Build, Test, and Development Commands
- `uv sync` installs and locks Python dependencies using the required uv toolchain.
- `./run.sh` bootstraps environment variables, warns about missing API keys, and launches the dev server.
- `uv run uvicorn backend.app:app --reload --port 8000` manually starts the API when you need finer control or debugging.
- `uv run pytest backend/tests` executes the backend test suite; add `-k name` for focused runs.

## Coding Style & Naming Conventions
Write Python against 3.13 with 4-space indentation, type hints, and docstrings where they clarify intent. Use `snake_case` for functions and variables, `PascalCase` for classes, and keep modules cohesive by feature. Prefer pure functions inside `rag_system.py` helpers to ease mocking. In `frontend/script.js`, stick to modern ES syntax, `const`/`let`, and descriptive event handler names; CSS classes in `style.css` follow kebab-case.

## Testing Guidelines
pytest with `pytest-mock` powers the suite. Mirror new modules with `test_*.py` files under `backend/tests/`, covering both success and failure paths. When touching ChromaDB integrations, seed lightweight fixtures instead of relying on the persisted `chroma_db/` directory. Include regression cases for prompt formatting and session handling before shipping.

## Commit & Pull Request Guidelines
Recent history favors concise, descriptive messages (for example, `backend: tighten session cleanup`). Use the imperative mood, mention the component, and group related changes into one commit. Pull requests should explain the problem, outline the solution, link any tracking issues, and list the commands you ran (tests, lint, manual checks). Attach screenshots or GIFs whenever frontend behavior shifts.

## Configuration & Secrets
Keep API keys in a root `.env` file (`PERPLEXITY_API_KEY`, optionally `OPENAI_API_KEY`) and never commit it. Document any new settings inside `backend/config.py` plus this guide, and provide sane fallbacks so the app still boots in a fresh clone.
