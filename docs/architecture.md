# Architecture

```mermaid
flowchart LR
  Operator[Factory users] --> Web[Next.js dashboard]
  Web --> API[FastAPI API]
  API --> PG[(PostgreSQL)]
  API --> Redis[(Redis)]
  MQTT[MQTT / OPC-UA gateway] --> API
  API --> CV[Vision inference]
  API --> RAG[RAG / LLM adapter]
  API --> Reports[PDF export]
  RAG --> Docs[(SOPs and logs)]
```

The API is stateless and uses PostgreSQL as the system of record. Redis is reserved for rate limits, asynchronous work, WebSocket fan-out, and cached analytics. MQTT ingestion must validate and normalize every message before persistence. AI model inference belongs behind adapters so an OpenAI, Ollama, or on-premise provider can be selected by environment.

## Entity relationships

```mermaid
erDiagram
  USERS ||--o{ AUDIT_LOGS : creates
  USERS ||--o{ CHAT_MESSAGES : asks
  MACHINES ||--o{ SENSOR_READINGS : emits
  MACHINES ||--o{ MAINTENANCE_RECORDS : requires
  MACHINES ||--o{ ALERTS : raises
  MACHINES ||--o{ ENERGY_READINGS : consumes
  PRODUCTION_ORDERS }o--|| PRODUCTS : produces
  DOCUMENTS ||--o{ CHAT_MESSAGES : grounds
  DEFECT_INSPECTIONS }o--|| PRODUCTS : inspects
  USERS ||--o{ REPORTS : generates
```
