# Container Deployment

The repository-level `docker-compose.yml` starts the dashboard, API, PostgreSQL, Redis, and MQTT broker. The frontend image accepts `NEXT_PUBLIC_API_URL` as a build argument because Next.js exposes public environment variables at build time.

For production, replace local Compose services with managed PostgreSQL and Redis, pass secrets through the platform secret store, and publish the images behind an HTTPS ingress.
