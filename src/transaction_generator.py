from typing import Generator
import logging
import time

from builders.customer_builder import CustomerBuilder
from builders.transaction_builder import TransactionBuilder
from fraud_engine import FraudEngine
from schemas.transaction import Transaction

logger = logging.getLogger(__name__)


def get_transaction(
    transaction_builder: TransactionBuilder,
    customer_builder: CustomerBuilder,
    fraud_engine: FraudEngine,
    publish_interval: float = 1.0,
    topic_name: str = "transactions",
) -> Generator[Transaction, None, None]:
    """Generates and processes transactions continuously.

    Args:
        transaction_builder: Builder instance for creating transactions.
        customer_builder: Builder instance to fetch customer pool.
        fraud_engine: Engine to evaluate/decorate transactions for fraud.
        publish_interval: Sleep duration (in seconds) between yields.
        topic_name: Target Kafka topic name for log context.

    Yields:
        Transaction: Processed transaction objects ready for downstream consumption.
    """
    logger.info("Initializing customer pool...")
    customers = customer_builder.build_customers()
    logger.info("Transaction generator started.")

    try:
        while True:
            normal_transaction = transaction_builder.build_normal_transaction(customers)
            if not normal_transaction:
                logger.warning("Failed to build transaction. Skipping cycle.")
                continue

            fraud_transactions = fraud_engine.process(normal_transaction)

            for transaction in fraud_transactions:
                logger.info(
                    f"Publishing transaction [%s] to kafka topic [%s] - Pause {publish_interval} sec",
                    transaction.id,
                    topic_name,
                )
                yield transaction
                if publish_interval > 0:
                    time.sleep(publish_interval)

    except KeyboardInterrupt:
        logger.info("Transaction generator stopped by user.")
    except Exception as e:
        logger.error("Unexpected error in transaction generator: %s", e, exc_info=True)
        raise
