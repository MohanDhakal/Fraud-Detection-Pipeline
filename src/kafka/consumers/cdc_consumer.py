from confluent_kafka import Consumer, KafkaException
import json


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
                key = self._decode_kafka_data(msg.key())

                # Kafka message value -> Python dict
                value = self._decode_kafka_data(msg.value())

                print("=" * 80)

                print(f"Topic     : {msg.topic()}")
                print(f"Partition : {msg.partition()}")
                print(f"Offset    : {msg.offset()}")

                print("\nKafka Key:")
                print(json.dumps(key, indent=4))

                print("\nKafka Value:")
                print(json.dumps(value, indent=4))

                print("=" * 80)

        except KeyboardInterrupt:
            print("\nStopping consumer...")

        finally:
            self.consumer.close()
