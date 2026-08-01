import json
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class MqttTelemetryBridge:
    """Configurable MQTT bridge; HTTP ingestion remains available when no broker is configured."""

    def start(self) -> None:
        settings = get_settings()
        if not settings.mqtt_broker_host:
            logger.info("MQTT bridge disabled: no broker configured")
            return
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            logger.warning("MQTT bridge disabled: paho-mqtt is not installed")
            return

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.connect_async(settings.mqtt_broker_host, settings.mqtt_broker_port)
        client.loop_start()
        logger.info("MQTT telemetry bridge started")

    @staticmethod
    def _on_connect(
        client: object, _userdata: object, _flags: object, _reason_code: object, _properties: object
    ) -> None:
        client.subscribe("factory/+/telemetry")

    @staticmethod
    def _on_message(_client: object, _userdata: object, message: object) -> None:
        payload = json.loads(message.payload.decode("utf-8"))
        logger.info("Received MQTT telemetry payload for machine %s", payload.get("machine_code"))
