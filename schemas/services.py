from dataclasses import dataclass
from dataclasses_avroschema import AvroModel


class Services(AvroModel):
    pass


@dataclass
class WalletLoad(Services):
    wallet_identifier: str
    wallet_provider_id: str
    route_id: str


@dataclass
class P2P(Services):
    bank_id: str
    route_id: str
    bank_acc_no: str


@dataclass
class MerchPay(Services):
    merchant_id: str
    acquirer_id: str
