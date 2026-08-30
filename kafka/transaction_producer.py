import logging
from typing import Generator
from confluent_kafka import Producer
from schemas.transaction import Transaction

logger = logging.getLogger("producer")


class TransactionProducer(Producer):
    def __init__(self, bootstrap_server: str):
        super().__init__({"bootstrap.servers": bootstrap_server})

    def publish(
        self,
        topic: str,
        transaction_stream: Generator[Transaction, None, None],
    ):
        try:
            for transaction in transaction_stream:
                payload = transaction.serialize()
                self.produce(topic=topic, value=payload)
        except Exception as e:
            logger.critical(
                "Pipeline crashed unexpectedly: %s",
                e,
                exc_info=True,
            )
        finally:
            logger.info("Cleaning up resources (flushing Kafka producers)...")
            logger.info("Pipeline stopped successfully.")
            self.flush()
