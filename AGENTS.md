# Repository Guidelines

## Project Structure & Module Organization

This is a standard test-flow system with a Vue 3 frontend and FastAPI backend.

- `frontend/src/views/` contains route-level pages; put reusable UI in `components/`, request wrappers in `api/`, shared state in `stores/`, and routing in `router/`.
- `backend/app/api/` holds FastAPI routers, `models/` SQLAlchemy entities, `schemas/` Pydantic request/response models, `services/` business operations, and `core/` configuration, authentication, and database code.
- `backend/alembic/` contains database migration tooling. Deployment configuration lives in `docker-compose.yml` and the two `Dockerfile`s.

Keep a feature's frontend API wrapper, view, router entry, backend router, schema, and model aligned. For example, project work belongs in `frontend/src/api/project.ts` and the corresponding `backend/app/{api,models,schemas}/project.py` files.

## Build, Test, and Development Commands

Run the full stack with Docker:

```bash
docker-compose up -d --build   # build and start MySQL, API, and web app
docker-compose logs -f backend # follow API logs
docker-compose down            # stop services (preserves volumes)
```

For local development, start MySQL with `docker-compose up -d mysql`, then run `pip install -r requirements.txt` and `uvicorn app.main:app --reload --port 8000` from `backend/`. From `frontend/`, run `npm install`, `npm run dev`, `npm run type-check`, and `npm run build`.

## Coding Style & Naming Conventions

Follow the surrounding code. Python uses four-space indentation, `snake_case` modules/functions, PascalCase models and schemas, typed async FastAPI handlers, and imports grouped at the top. TypeScript uses two-space indentation, `camelCase` functions/variables, PascalCase Vue components, and `<script setup lang="ts">`. Keep API paths plural (for example, `/projects`) and use Pydantic schemas rather than returning ORM objects directly.

## Testing Guidelines

No automated test suite is currently configured. At minimum, run `npm run type-check` and `npm run build` for frontend changes, and exercise changed API endpoints through `http://localhost:8000/docs`. Add focused tests alongside the relevant layer when introducing non-trivial logic; name Python tests `test_*.py` and frontend tests `*.spec.ts` if a test runner is added.

## Commit & Pull Request Guidelines

Use the repository's Conventional Commit pattern: `feat: ...` for additions and `fix: ...` for corrections; concise Chinese summaries are established practice. Keep commits focused. Pull requests should state the affected module, user-visible behavior, verification commands, linked issue if available, and screenshots for UI changes.

## Configuration & Security

Copy `backend/.env.example` to `backend/.env` for local secrets. Never commit credentials, generated uploads, or production keys. Treat `docker-compose.yml` passwords and the default admin account as development-only values.
