from confluent_kafka import Consumer, KafkaException
import json
import base64
from decimal import Decimal


class CdcConsumer(Consumer):
    def __init__(self, bootstrap_server: str, group_id: str):
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_server,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
            }
        )

    def _decode_kafka_data(self, data):
        """Decode Kafka key/value bytes into a Python object."""
        if data is None:
            return None

        decoded = data.decode("utf-8")

        try:
            return json.loads(decoded)
        except json.JSONDecodeError:
            return decoded

    def consume_events(self, topic: str):
        self.consumer.subscribe([topic])
        print(f"Listening to: {topic}")
        print("Waiting for PostgreSQL changes...\n")
        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    raise KafkaException(msg.error())

                # Kafka message key -> Python object
                # key = self._decode_kafka_data(msg.key())

                # Kafka message value -> Python dict
                event = self._decode_kafka_data(msg.value())

                # print("\nKafka Key:")
                # print(json.dumps(key, indent=4))
                payload = event.get("payload", event)
                operation = payload.get("op")

                if operation in ("c", "u"):
                    transaction = payload.get("after")
                    if transaction["is_fraud"]:
                        print("=" * 80)

                        print(f"Topic     : {msg.topic()}")
                        print(f"Partition : {msg.partition()}")
                        print(f"Offset    : {msg.offset()}")

                        raw_bytes = base64.b64decode(transaction["amount"])
                        unscaled = int.from_bytes(
                            raw_bytes, byteorder="big", signed=True
                        )
                        amount = Decimal(unscaled)
                        record = {
                            "id": transaction["id"],
                            "customer_id": transaction["customer_id"],
                            "amount": amount,
                            "timestamp": transaction["timestamp"],
                            "location_name": transaction["location_name"],
                            "ip_address": transaction["ip_address"],
                            "currency": transaction["currency"],
                            "device_id": transaction["device_id"],
                            "is_fraud": transaction["is_fraud"],
                            "fraud_type": transaction["fraud_type"],
                            "service_name": transaction["service_name"],
                        }

                        print(record)
                        print("=" * 80)
                    else:
                        print(
                            f'Transaction {transaction["id"]} and Fraud Type {transaction['service_name']}'
                        ),

        except KeyboardInterrupt:
            print("\nStopping consumer...")

        finally:
            self.consumer.close()
