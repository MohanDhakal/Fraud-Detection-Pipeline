from dataclasses import dataclass
from datetime import datetime
from dataclasses_avroschema import AvroModel
from schemas.location import LocationLatLong

from schemas.fake_bank import FakeBank
from schemas.fake_wallet import FakeWallet


@dataclass
class Customer(AvroModel):
    id: str
    name: str
    msisdn: str
    created_on: datetime
    device_id: str = None
    location: LocationLatLong = None
    email: str = None
    bank: FakeBank = None
    wallet: FakeWallet = None
    wallet_id: str = None
    bank_acc_no: str = None
    usual_ip: str = None
