# API Guide

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

| Area | Endpoint | Purpose |
| --- | --- | --- |
| Authentication | `POST /api/v1/auth/login` | Returns access and refresh tokens |
| Dashboard | `GET /api/v1/analytics/dashboard` | Returns KPI, chart, fleet, and alert data |
| Assets | `GET /api/v1/machines` | Returns machine health and status |
| Products | `GET /api/v1/products` | Returns the catalog used by orders and inspection |
| Telemetry | `GET /api/v1/sensors` | Returns the most recent sensor readings |
| Maintenance | `GET /api/v1/maintenance` | Returns scheduled and predictive work |
| Quality | `POST /api/v1/vision/inspect` | Runs an inspection request |
| Copilot | `POST /api/v1/chat` | Answers a grounded factory question |
| Reports | `POST /api/v1/reports/pdf` | Downloads an executive, machine, or energy PDF |

All endpoints except `/healthz` and authentication routes require `Authorization: Bearer <access-token>`. Inspection, reporting, user management, and settings additionally enforce role permissions.
