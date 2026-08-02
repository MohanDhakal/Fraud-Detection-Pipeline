import random
from schemas.fraud.fraud_scenario import (
    AccountTakeover,
    SimSwap,
    VelocityAttack,
)
from schemas.transaction import Transaction
from config.producer_config import FraudConfig
from config.consumer_config import ConsumerConfig


class FraudEngine:
    def __init__(
        self,
        producer_config: FraudConfig = None,
        consumer_config: ConsumerConfig = None,
    ):
        self.config = producer_config
        self.consumer_config = consumer_config

    def process(self, transaction) -> list[Transaction]:
        probability = self.config.injection_probability
        current_probability = random.random()
        if current_probability > probability:
            return [transaction]
        scene_config = random.choice(self.config.scenarios)
        filtered_transactions: list[Transaction] = []
        if scene_config.type == "account_takeover":
            filtered_transactions = AccountTakeover(
                producer_fraud_config=scene_config,
            ).generate(
                transaction=transaction,
                current_prob=current_probability,
            )
        elif scene_config.type == "velocity_attack":
            filtered_transactions = VelocityAttack(
                producer_fraud_config=scene_config,
            ).generate(transaction=transaction)
        elif scene_config.type == "sim_swap":
            filtered_transactions = SimSwap(
                producer_fraud_config=scene_config,
            ).generate(
                transaction=transaction,
                current_prob=current_probability,
            )
        return filtered_transactions

    def check_account_takeover_fraud(
        self,
        transaction: Transaction,
    ) -> bool:

        takeover_fraud = AccountTakeover(
            consumer_config=self.consumer_config,
        )
        possible_at_fraud = takeover_fraud.detect(transaction=transaction)
        return possible_at_fraud

    def check_velocity_attact_fraud(self, transactions: list[Transaction]) -> bool:
        velocity_attack_fraud = VelocityAttack(
            consumer_config=self.consumer_config,
        )
        possible_va_fraud = velocity_attack_fraud.detect(transactions=transactions)
        return possible_va_fraud

    def can_add_to_history(
        self,
        transaction: Transaction,
        customer_history: list[Transaction] = None,
    ) -> bool:
        if customer_history is None:
            return False
        velocity_attack_fraud = VelocityAttack(
            consumer_config=self.consumer_config,
        )
        can_add = velocity_attack_fraud.add_to_history(
            transaction=transaction,
            customer_history=customer_history,
        )
        return can_add

    def check_sim_swap_fraud(self, transaction: Transaction) -> bool:
        sim_swap_fraud = SimSwap(
            consumer_config=self.consumer_config,
        )

        return sim_swap_fraud.detect(transaction=transaction)
