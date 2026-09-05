from venv import logger
from confluent_kafka import Consumer, KafkaError
from fraud_engine import FraudEngine
from kafka.consumers.services.db_service import DBService
from schemas.services import P2P, MerchPay
from schemas.transaction import Transaction
from psycopg2 import sql


class SaveTransactionConsumer(Consumer):

    def __init__(
        self,
        bootstrap_server: str,
        group_id: str,
        topic: str,
        db_service: DBService,
        fraud_engine: FraudEngine,
    ):
        self.topic = topic
        self.db_service = db_service
        self.total_transactions: int = 0
        self.fraud_engine = fraud_engine
        self.customer_history: list[Transaction] = None

        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_server,
                "group.id": group_id,
                # This setting is used only when the consumer group has no committed offset for a partition.
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,  # disable in id
            }
        )

    def consume(self, conn):
        logger.info("Saving Transactions")
        self.consumer.subscribe([self.topic])
        try:
            print("Waiting 1 Second For Message To Arrive...")
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error(msg.error())
                    continue
                transaction = Transaction.deserialize(msg.value())
                self._save_transaction(conn, transaction)
                self.consumer.commit(message=msg)
                logger.info(
                    f"Message Received | "
                    f"Topic: {msg.topic()} | "
                    f"Partition: {msg.partition()} | "
                    f"Transaction ID: {Transaction.deserialize(msg.value()).id}"
                )
        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt Received,Stopping Consumer ....")
        finally:
            self.consumer.close()

    def clean_tables(self, conn):
        try:
            delete_records = "DELETE FROM {}"
            query = sql.SQL(delete_records).format(sql.Identifier("transaction"))
            self.db_service.clean_tablespace(query=query, conn=conn)
        except Exception as e:
            logger.error(f"Error cleaning up tables {e}")
            conn.close()

    def _save_transaction(self, conn, transaction: Transaction):
        add_loc_query = """
                            INSERT INTO {}
                            (id,customer_id,amount,timestamp, location_name, ip_address, service_name, currency, device_id)
                            VALUES
                            (
                            %s,%s,%s,%s,%s,%s,%s,%s,%s
                            )
                        """
        query = sql.SQL(add_loc_query).format(sql.Identifier("transaction"))
        service_name = (
            "p2p"
            if isinstance(transaction.service_obj, P2P)
            else (
                "merch_pay"
                if isinstance(transaction.service_obj, MerchPay)
                else "wallet_load"
            )
        )
        self.db_service.execute_query(
            query=query,
            conn=conn,
            values=(
                transaction.id,
                transaction.customer.id,
                transaction.amount,
                transaction.timestamp,
                transaction.location.name,
                transaction.ip_address,
                service_name,
                transaction.currency,
                transaction.device_id,
            ),
        )
        self._process_and_record_fraud(transaction=transaction, conn=conn)

    def _process_and_record_fraud(self, conn, transaction: Transaction):
        current_total = self.total_transactions
        self.total_transactions = current_total + 1
        fraud_type: str = None
        # accout takeover check
        is_at_fraud = self.fraud_engine.check_account_takeover_fraud(
            transaction=transaction
        )

        if is_at_fraud:
            print(f"Updating Account Takeover - Transaction ID: {transaction.id}")
            fraud_type = "account_takeover"
        # sim swap fraud

        is_sim_swap_fraud = self.fraud_engine.check_sim_swap_fraud(
            transaction=transaction
        )
        if is_sim_swap_fraud:
            print(f"Updating Sim Swap - Transaction ID: {transaction.id}")
            fraud_type = "sim_swap"

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
                print(
                    f"Updating Velocity Attack - Transaction with ID: {transaction.id}\n"
                )
                fraud_type = "velocity_attack"
        if fraud_type is not None:
            self._update_fraud_flag(
                transaction_id=transaction.id,
                fraud_type=fraud_type,
                conn=conn,
            )

    def _update_fraud_flag(self, conn, transaction_id: str, fraud_type: str):
        values = (True, fraud_type, transaction_id)
        update_fraud_query = """
                            UPDATE {}
                            SET is_fraud = %s,
                                fraud_type = %s
                            WHERE id = %s
                            """
        query = sql.SQL(update_fraud_query).format(sql.Identifier("transaction"))
        self.db_service.execute_query(query=query, conn=conn, values=values)
