from pydantic.dataclasses import dataclass


@dataclass
class AmountRange:
    min: int
    max: int


@dataclass
class TransactionCount:
    min: int
    max: int


@dataclass
class ServiceLimits:
    wallet_load: AmountRange
    p2p: AmountRange
    merch_pay: AmountRange


@dataclass
class AccountTakeoverConfig:
    services: ServiceLimits


@dataclass
class VelocityAttackConfig:
    transaction_count: TransactionCount
    interval_seconds: int


@dataclass
class SimSwapConfig:
    services: ServiceLimits


@dataclass
class FraudDetectionConfig:
    account_takeover: AccountTakeoverConfig
    velocity_attack: VelocityAttackConfig
    sim_swap: SimSwapConfig


@dataclass
class ConsumerConfig:
    fraud_detection: FraudDetectionConfig
