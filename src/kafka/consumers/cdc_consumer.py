from typing import Any

from confluent_kafka import Consumer, KafkaException
import json
import base64
from decimal import Decimal

from kafka.consumers.services.cloud_service import CloudService, logger


class CloudUploadException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


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
        aws_cloud = CloudService()
        s3_client = CloudService.setup_s3_client()

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

                # printing the results

                if operation in ("c", "u", "d"):
                    transaction_without_read = payload
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
                    # sending whole payload to the cloud
                self.upload_to_cloud(
                    record=transaction_without_read,
                    s3_client=s3_client,
                    aws_service=aws_cloud,
                )
        except CloudUploadException as e:
            print(f"\nCloud Upload Failed with ... :{e.message}")
        except KeyboardInterrupt:
            print("\nStopping consumer due to keyboard interruption...")
        finally:
            self.consumer.close()

    def upload_to_cloud(
        self,
        record: dict[str, Any],
        aws_service: CloudService,
        s3_client,
    ):
        response = aws_service.upload_to_s3(
            table_name="cdc_transactions",
            client=s3_client,
            data=record,
        )
        if response.get("error") is not None:
            raise CloudUploadException(message=response.get("error"))
        if response.get("msg") is not None:
            logger.info(f"MetaData: ${response.get('msg')}")
