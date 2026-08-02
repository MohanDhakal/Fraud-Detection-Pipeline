from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from datetime import timedelta
import random
from config.consumer_config import ConsumerConfig
from config.producer_config import FraudScenarioConfig, ProducerConfig
from data.nepal_data_provider import NepalDataProvider
from schemas.customer import Customer
from schemas.services import P2P, MerchPay, WalletLoad
from schemas.transaction import Transaction
from faker import Faker
from collections import defaultdict, deque
from datetime import timedelta

fake = Faker()
fake.add_provider(NepalDataProvider)


@dataclass
class FraudScenario(ABC):
    @abstractmethod
    def generate(self, transction):
        pass


class AccountTakeover(FraudScenario):
    # some egs.
    # differnt IP, different locatio, unusual amount, different device, high-risk merchants etc
    def __init__(
        self,
        producer_fraud_config: FraudScenarioConfig = None,
        consumer_config: ConsumerConfig = None,
    ):
        self.producer_fraud_config = producer_fraud_config
        self.consumer_config = consumer_config

    def generate(self, transaction: Transaction, current_prob: float):
        new_location_probability = self.producer_fraud_config.params[
            "new_location_probability"
        ]
        if current_prob * 1.2 <= new_location_probability:
            transaction.location = fake.location()

        new_ip_probability = self.producer_fraud_config.params["new_ip_probability"]
        if current_prob * 1.5 <= new_ip_probability:
            transaction.ip_address = fake.ipv4()

        # need to confirm lower and upper limit of the amount
        transaction.amount *= random.randint(3, 10)
        transaction.is_fraud = True
        transaction.fraud_type = "account_takeover"
        return [transaction]

    def detect(
        self,
        transaction: Transaction,
    ) -> bool:
        list_of_fraud_indicators: list[bool] = []
        # transaction information
        transaction_ip = transaction.ip_address
        transaction_location = transaction.location
        transaction_device_id = transaction.device_id
        # customer information
        customer = transaction.customer
        customer_device_id = customer.device_id
        customer_ip = customer.usual_ip
        customer_location = customer.location
        # service
        service = transaction.service_obj
        max_limit = 0
        min_limit = 0
        transaction_amount = transaction.amount
        fraud_config = self.consumer_config.fraud_detection.account_takeover

        if isinstance(service, WalletLoad):
            wallet_load_config = fraud_config.services.wallet_load
            max_limit = wallet_load_config.max
            min_limit = wallet_load_config.min
        elif isinstance(service, MerchPay):
            merchpay_config = fraud_config.services.merch_pay
            max_limit = merchpay_config.max
            min_limit = merchpay_config.min
        elif isinstance(service, P2P):
            p2p_config = fraud_config.services.p2p
            max_limit = p2p_config.max
            min_limit = p2p_config.min

        if transaction_ip != customer_ip:
            list_of_fraud_indicators.append(True)
        if transaction_location != customer_location:
            list_of_fraud_indicators.append(True)
        if transaction_device_id != customer_device_id:
            list_of_fraud_indicators.append(True)
        if transaction_amount > min_limit:
            list_of_fraud_indicators.append(True)
        if transaction_amount < max_limit:
            list_of_fraud_indicators.append(True)
        return list_of_fraud_indicators.count(True) > 2


class VelocityAttack(FraudScenario):
    def __init__(
        self,
        producer_fraud_config: FraudScenarioConfig = None,
        consumer_config: ConsumerConfig = None,
    ):
        self.producer_fraud_config = producer_fraud_config
        self.consumer_config = consumer_config

    def generate(self, transaction: Transaction):
        config = self.producer_fraud_config
        txns = []
        count = random.randint(
            config.params["transaction_count"][0],
            config.params["transaction_count"][1],
        )
        interval = config.params["interval_seconds"]
        for i in range(count):
            tx = deepcopy(transaction)
            tx.id = fake.uuid4()
            tx.timestamp = transaction.timestamp + timedelta(seconds=i * interval)
            tx.is_fraud = True
            tx.fraud_type = "velocity_attack"
            txns.append(tx)
        return txns

    def detect(self, transactions: list[Transaction]) -> False:
        is_fraud = False
        fraud_config = self.consumer_config.fraud_detection.velocity_attack
        expected_trans_interval = fraud_config.interval_seconds
        min_to_enable_check = fraud_config.transaction_count.min
        #    upper_limit = fraud_config.transaction_count.max
        transactions.sort(key=lambda item: item.timestamp)
        last_transaction = transactions[-1]
        first_transaction = transactions[0]
        time_diff = (
            last_transaction.timestamp - first_transaction.timestamp
        ).total_seconds()
        if transactions.count() >= min_to_enable_check:
            if time_diff > 0 and time_diff <= expected_trans_interval:
                is_fraud = True
        return is_fraud

    def add_to_history(
        self,
        transaction: Transaction,
        customer_history: list[Transaction],
    ):
        add = False
        customer_transaction_count = len(customer_history)
        fraud_config = self.consumer_config.fraud_detection.velocity_attack
        expected_trans_interval = fraud_config.interval_seconds
        min_to_enable_check = fraud_config.transaction_count.min

        if customer_transaction_count > 0:
            if customer_transaction_count > min_to_enable_check:
                # check for fraud and reset history
                customer_history[:] = transaction
            elif customer_history[0].customer.id == transaction.customer.id:
                last_history_record_time = customer_history[-1].timestamp
                new_record_time = transaction.timestamp
                time_diff = new_record_time - last_history_record_time
                if time_diff.total_seconds() <= expected_trans_interval:
                    add = True
            else:
                customer_history[:] = transaction

        else:
            add = True
        return add


class SimSwap(FraudScenario):
    def __init__(
        self,
        producer_fraud_config: FraudScenarioConfig = None,
        consumer_config: ConsumerConfig = None,
    ):
        self.producer_fraud_config = producer_fraud_config
        self.consumer_config = consumer_config

    def generate(
        self,
        transaction: Transaction,
        current_prob: float,
    ):
        new_device_probability = self.producer_fraud_config.params[
            "new_device_probability"
        ]
        if current_prob * 1.2 <= new_device_probability:
            transaction.device_id = fake.uuid4()
        transaction.amount *= 2
        transaction.is_fraud = True
        transaction.fraud_type = "sim_swap"

        return [transaction]

    def detect(self, transaction: Transaction) -> bool:
        # transaction information
        transaction_device_id = transaction.device_id
        customer = transaction.customer
        # customer information
        customer_device_id = customer.device_id
        # service
        service = transaction.service_obj
        max_limit = 0
        min_limit = 0
        transaction_amount = transaction.amount
        fraud_config = self.consumer_config.fraud_detection.sim_swap

        if isinstance(service, WalletLoad):
            wallet_load_config = fraud_config.services.wallet_load
            max_limit = wallet_load_config.max
            min_limit = wallet_load_config.min
        elif isinstance(service, MerchPay):
            merchpay_config = fraud_config.services.merch_pay
            max_limit = merchpay_config.max
            min_limit = merchpay_config.min
        elif isinstance(service, P2P):
            p2p_config = fraud_config.services.p2p
            max_limit = p2p_config.max
            min_limit = p2p_config.min
        # unusual transaction from the new device
        return transaction_device_id != customer_device_id and (
            transaction_amount > max_limit or transaction_amount < min_limit
        )
