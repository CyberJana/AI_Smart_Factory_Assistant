# Industrial Connectivity

The MQTT bridge listens on `factory/{machine_code}/telemetry`; payloads should contain `machine_code`, metric values, and an ISO-8601 timestamp. Implement the OPC-UA adapter beside `backend/app/services/iot.py`, with certificate-based authentication and a mapping layer that normalizes tag names before persistence.
