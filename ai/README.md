# AI Pipeline

The API uses a deterministic, document-grounded fallback in `backend/app/services/copilot.py` for demonstrations. Configure an OpenAI or Ollama adapter in that service for managed or local LLM inference. The `ai` optional dependency group contains LangChain and FAISS dependencies for semantic retrieval.

Predictive maintenance training should ingest `database/sample_sensor_data.csv`, version features and labels, evaluate against a held-out time series, and register models before exposing predictions to operators.
