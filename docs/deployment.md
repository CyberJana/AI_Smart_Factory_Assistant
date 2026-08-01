# Deployment Guide

## Local demonstration

1. Copy `backend/.env.example` to `backend/.env` and set a random `JWT_SECRET`.
2. Run `docker compose up --build`.
3. Open `http://localhost:3000` and sign in with `admin@smartfactory.example` / `ChangeMe123!`.

## Production checklist

- Use managed PostgreSQL and Redis with private networking, backups, point-in-time recovery, TLS, and least-privilege service accounts.
- Store secrets in a cloud secret manager; never use the Compose defaults outside development.
- Terminate HTTPS at a managed ingress and restrict CORS to approved dashboard origins.
- Move browser token storage to secure, HttpOnly, SameSite cookies when adding a server-side session or BFF layer.
- Run database migrations through CI/CD instead of startup schema creation.
- Place model workers, MQTT ingestion, and report generation on separate autoscaled workloads.
- Configure centralized structured logs, metrics, traces, alert routing, vulnerability scanning, and retention policies.
- Use a durable task queue for notification delivery and long-running ML/CV jobs.

## Roadmap

1. Add Alembic migrations, token rotation/revocation, password reset, and verified email delivery.
2. Add OPC-UA, a persistent MQTT consumer, Redis event fan-out, and real-time WebSocket dashboards.
3. Register trained RUL/anomaly and YOLO models with model/version monitoring.
4. Add tenant isolation, SSO/SAML, signed exports, and enterprise audit retention.
