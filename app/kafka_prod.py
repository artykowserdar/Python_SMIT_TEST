import json
from confluent_kafka import Producer
import os
from datetime import datetime

# Конфигурация Kafka producer
producer_config = {
    "bootstrap.servers": os.getenv("KAFKA_BROKER", "localhost:9092"),
    "client.id": "insurance-api",
}

producer = Producer(producer_config)


# Логирование изменений в Kafka
def log_to_kafka(user_id: int, action: str, info: str):
    message = {
        "user_id": user_id,
        "action": action,
        "info": info,
        "create_ts": datetime.utcnow().isoformat(),
    }
    producer.produce(
        topic="insurance_logs",
        key=str(user_id),
        value=json.dumps(message),
    )
    producer.flush()
