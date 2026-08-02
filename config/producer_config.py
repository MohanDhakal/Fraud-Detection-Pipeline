from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional


# -------------------------
# Generator
# -------------------------
@dataclass
class GeneratorConfig:
    throughput_tps: float
    duration_minutes: Optional[int] = None
    seed: int = 42


# -------------------------
# Customers
# -------------------------


@dataclass
class CustomersConfig:
    count: int


# -------------------------
# Amount / Distribution
# -------------------------


@dataclass
class NormalAmount:
    min: int
    max: int


@dataclass
class Distribution:
    type: str
    alpha: Optional[float] = None
    beta: Optional[float] = None
    mode: Optional[int] = None


@dataclass
class AmountConfig:
    normal: NormalAmount
    distribution: Distribution


# -------------------------
# Services
# -------------------------


@dataclass
class WalletLoadConfig:
    amount: AmountConfig


@dataclass
class P2PConfig:
    amount: AmountConfig


@dataclass
class MerchPayConfig:
    amount: AmountConfig


@dataclass
class ServicesConfig:
    wallet_load: WalletLoadConfig
    p2p: P2PConfig
    merch_pay: MerchPayConfig


# -------------------------
# Fraud Configs
# -------------------------


@dataclass
class FraudScenarioConfig:
    type: str
    weight: int
    params: dict = field(default_factory=dict)


@dataclass
class FraudConfig:
    injection_probability: float
    scenarios: list[FraudScenarioConfig]


@dataclass
class ProducerConfig:
    generator: GeneratorConfig
    customers: CustomersConfig
    services: ServicesConfig
    fraud: FraudConfig
