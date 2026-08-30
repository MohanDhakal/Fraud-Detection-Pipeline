import logging
from builders.customer_builder import CustomerBuilder
from builders.transaction_builder import TransactionBuilder
from config_loader import load_config, load_consumer_config
from consts.constants import FileLocation
from fraud_engine import FraudEngine
from kafka.transaction_consumer import TransactionConsumer
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


def run_consumer():
    fraud_detector = FraudEngine(
        consumer_config=load_consumer_config(
            config_path=FileLocation.consumer_config_file,
        )
    )
    consumer = TransactionConsumer(
        bootstrap_server=FileLocation.kafka_bootstrap_server,
        group_id="fraud_detectors-v2",
        topic="transactions",
        fraud_detector=fraud_detector,
    )

    consumer.consume()


if __name__ == "__main__":
    message = """What do you want to run ?
    --------------------------------------
        1. Producer for topic 
        2. Consumer for topic 
        """
    option = int(input(message))
    if option == 1:
        print("Producer Selected...")
        run_producer()
    elif option == 2:
        print("Consumer Selected...")
        run_consumer()
