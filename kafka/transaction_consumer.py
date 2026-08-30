import logging
from venv import logger

from confluent_kafka import Consumer, KafkaError
from fraud_engine import FraudEngine
from schemas.transaction import Transaction

logger = logging.getLogger("consumer")


class TransactionConsumer:

    def __init__(
        self,
        bootstrap_server: str,
        group_id: str,
        topic: str,
        fraud_detector: FraudEngine,
    ):
        self.topic = topic
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_server,
                "group.id": group_id,
                # This setting is used only when the consumer group has no committed offset for a partition.
                "auto.offset.reset": "latest",  # or "latest"
                "enable.auto.commit": False,  # disable in production
            }
        )
        self.customer_history: list[Transaction] = None
        self.total_transactions: int = 0
        self.fraud_engine = fraud_detector

    def consume(self):
        primary_message = """"
        ----------------------------------------------------------------------------------------
        Fraud Detection System is sensing transactions...
        Once any type of fraud is detected, the system will print the fraud summary upto that time        
        -----------------------------------------------------------------------------------------
        """
        self.consumer.subscribe([self.topic])
        try:
            logger.info(primary_message)
            while True:
                # asks producer for any new messages, waits 1 second before continuing
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                # sometiemes kafka returns an error object like Broker Unavailable, Partition leader moved, Topic Deleted, Offset problem etc.
                if msg.error():
                    # if partition contains offset 0,1,2,3, and program has already reached 3, it simply waits for more message
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    # actual error -> log it and continue
                    logger.error(msg.error())
                    continue
                # kafka store bytes convert it to a real object
                transaction = Transaction.deserialize(msg.value())
                self.process(transaction)
                self.consumer.commit(message=msg)
        except KeyboardInterrupt:
            logger.info("Stopping Consumer ....")
        finally:
            self.consumer.close()

    def process(self, transaction: Transaction):
        current_total = self.total_transactions
        self.total_transactions = current_total + 1
        # accout takeover check
        is_at_fraud = self.fraud_engine.check_account_takeover_fraud(
            transaction=transaction
        )

        if is_at_fraud:
            separator = f"----------------------------Total Processed: {self.total_transactions}----------------------------"
            print(separator)
            print(f"Account Takeover - Transaction ID: {transaction.id}")
            logger.info(transaction.to_json())
            print(
                "---------------------------------------------------------------------------------------------------------"
            )

        # sim swap fraud
        is_sim_swap_fraud = self.fraud_engine.check_sim_swap_fraud(
            transaction=transaction
        )
        if is_sim_swap_fraud:
            separator = f"----------------------------Total Processed: {self.total_transactions}----------------------------"
            print(separator)
            print(f"Sim Swap - Transaction ID: {transaction.id}")
            logger.info(transaction.to_json())
            print(
                "---------------------------------------------------------------------------------------------------------"
            )

        # velocity attack check
        can_add = self.fraud_engine.can_add_to_history(
            transaction=transaction,
            customer_history=self.customer_history,
        )
        if can_add:

            is_va_fraud = self.fraud_engine.check_velocity_attact_fraud(
                transactions=self.customer_history
            )
            if is_va_fraud:
                separator = f"----------------------------Total Processed: {self.total_transactions}----------------------------"
                print(separator)
                print(f"Velocity Attack - Transaction with ID: {transaction.id}\n")
                logger.info(transaction.to_json())
                print(
                    "---------------------------------------------------------------------------------------------------------"
                )
