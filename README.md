# AI Smart Factory Assistant

ForgeSight is a containerized AI operations platform for manufacturing teams. It combines a Next.js command center with a secure FastAPI API, seeded plant data, operational analytics, vision inspection contracts, predictive-maintenance workflows, and a grounded Factory Copilot.

![Technology](https://img.shields.io/badge/stack-Next.js%20%7C%20FastAPI%20%7C%20PostgreSQL-17e5be)

## Included capabilities

- Role-aware JWT authentication and audited operational actions
- Fleet health, utilization, alarms, sensor telemetry, and WebSocket telemetry contract
- Predictive maintenance queue with health-risk context
- Quality inspection API contract with bounding boxes and confidence scores
- Production, inventory, low-stock, energy, quality, and OEE dashboard metrics
- Document-grounded Factory Copilot and generated PDF reports
- PostgreSQL schema, sample telemetry, Docker Compose, CI, API docs, and deployment guidance

## Quick start

```bash
cp backend/.env.example backend/.env
# Set JWT_SECRET to a random value before starting.
docker compose up --build
```

On PowerShell, use `Copy-Item backend\.env.example backend\.env` instead of `cp`.

Open `http://localhost:3000`, then sign in through `/login`:

```text
Email:    admin@smartfactory.example
Password: ChangeMe123!
```

The dashboard renders seeded data without credentials for a visual demonstration. Signing in switches it to the protected live API.

## Local development

```bash
# API
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Web
cd frontend
npm install
npm run dev
```

Run the backend suite with `pytest -q` from `backend`, and run frontend checks with `npm run typecheck && npm run build` from `frontend`.

## Project layout

```text
frontend/     Next.js App Router dashboard
backend/      FastAPI API, SQLAlchemy models, services, and tests
ai/           RAG and predictive-maintenance integration notes
vision/       CV inference integration notes
iot/          MQTT and OPC-UA integration notes
database/     Canonical schema and demo telemetry
docker/       Deployment extension point
docs/         Architecture, API, and deployment documentation
.github/      CI workflow
```

## Architecture and operations

- [Architecture and ER diagram](docs/architecture.md)
- [API guide](docs/api.md), with interactive OpenAPI at `/docs`
- [Deployment guide and roadmap](docs/deployment.md)

## Production hardening

This repository is intentionally runnable without factory hardware or paid AI keys. Before production, configure managed secrets and TLS, use migrations rather than startup schema creation, connect a durable MQTT/OPC-UA ingestion pipeline, replace demonstration AI adapters with versioned model services, and follow the deployment checklist.

## License

MIT