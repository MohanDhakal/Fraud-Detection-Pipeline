from dataclasses import dataclass
from datetime import datetime
from dataclasses_avroschema import AvroModel, types
from schemas.customer import Customer
from schemas.location import LocationLatLong
from schemas.services import Services


@dataclass
class Transaction(AvroModel):
    id: str
    customer: Customer
    amount: types.condecimal(
        max_digits=19,
        decimal_places=2,
    )  # type: ignore
    timestamp: datetime
    location: LocationLatLong
    ip_address: str
    service_obj: Services
    currency: str
    device_id: str
    is_fraud: bool = False
    fraud_type: str = None
