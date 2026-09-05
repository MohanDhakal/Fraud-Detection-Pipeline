import logging
from builders.customer_builder import CustomerBuilder
from builders.transaction_builder import TransactionBuilder
from config_loader import load_config, load_consumer_config
from consts.constants import FileLocation
from fraud_engine import FraudEngine
from kafka.consumers.fraud_detection_consumer import FraudDetectionConsumer

from kafka.consumers.save_transaction_consumer import SaveTransactionConsumer
from kafka.consumers.services.db_service import DBService
from kafka.transaction_producer import TransactionProducer
from transaction_generator import get_transaction
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def run_producer():
    config = load_config(config_path=FileLocation.config_file)
    logger.info("Generating Transactions...")
    throuhput = config.generator.throughput_tps
    wait_until_seconds = int(1 / throuhput)

    stream = get_transaction(
        transaction_builder=TransactionBuilder(),
        customer_builder=CustomerBuilder(),
        fraud_engine=FraudEngine(producer_config=config.fraud),
        publish_interval=wait_until_seconds,
        topic_name="transactions",
    )
    producer = TransactionProducer(bootstrap_server=FileLocation.kafka_bootstrap_server)
    logger.info("Pushing to Producer...")
    producer.publish(
        topic="transactions",
        transaction_stream=stream,
    )


def run_fraud_consumer():
    fraud_detector = FraudEngine(
        consumer_config=load_consumer_config(
            config_path=FileLocation.consumer_config_file,
        )
    )
    consumer = FraudDetectionConsumer(
        bootstrap_server=FileLocation.kafka_bootstrap_server,
        group_id="fraud_detectors-v2",
        topic="transactions",
        fraud_detector=fraud_detector,
    )

    consumer.consume()


def run_transaction_save_consumer():
    fraud_detector = FraudEngine(
        consumer_config=load_consumer_config(
            config_path=FileLocation.consumer_config_file,
        )
    )
    db_service = DBService()
    consumer = SaveTransactionConsumer(
        bootstrap_server=FileLocation.kafka_bootstrap_server,
        group_id="transactions_persistence_service_group",
        topic="transactions",
        db_service=db_service,
        fraud_engine=fraud_detector,
    )
    conn = db_service.get_db_connection()
    consumer.clean_tables(conn)
    consumer.consume(conn)


if __name__ == "__main__":
    message = """What do you want to run ?
    --------------------------------------
        1. Producer for topic transactions(Enter 1)
        2. Fraud Detection Consumer for topic transactions(Enter 2)
        3. Save Transaction Consumer for topic transactions(Enter 3)
        """
    option = int(input(message))
    match (option):
        case 1:
            run_producer()
        case 2:
            run_fraud_consumer()
        case 3:
            run_transaction_save_consumer()
