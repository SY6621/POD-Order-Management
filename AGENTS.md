## Cursor Cloud specific instructions

### Project overview

ETSY Order Automation System — a full-stack internal tool for managing Etsy e-commerce orders (email ingestion, order parsing, effect image generation, production docs, logistics). See `README.md` for general project info and `docs/frontend-backend-api.md` for DB schema and API docs.

### Services

| Service | Port | Start command |
|---------|------|---------------|
| FastAPI Backend | 8000 | `cd backend && poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload` |
| Vue3 Frontend (Vite) | 5173 | `cd frontend && npm run dev -- --host 0.0.0.0` |

### Running lint / tests / build

- **Backend lint**: `cd backend && poetry run black --check src/` and `cd backend && poetry run pylint src/ --exit-zero`
- **Backend tests**: `cd backend && poetry run pytest tests/ -v` (test directory exists but currently has no test files)
- **Frontend build**: `cd frontend && npm run build` (note: `Remote.vue` has a pre-existing duplicate `<script setup>` bug that breaks production builds; the dev server is unaffected)

### Gotchas

- `pycairo` requires system packages `libcairo2-dev`, `pkg-config`, and `python3-dev` to build from source. These are already installed in the VM snapshot.
- Both frontend and backend need `.env` files (see `.env.example` in each directory). Without real Supabase credentials, the frontend loads with mock/placeholder data and API calls to Supabase will fail.
- The frontend connects to Supabase directly **and** to the FastAPI backend at `localhost:8000` — both services should be running for full functionality.
- `backend/src/services/pdf_service_clean.py` has a non-UTF-8 byte sequence that causes `black` to fail on that file; this is a pre-existing issue.
