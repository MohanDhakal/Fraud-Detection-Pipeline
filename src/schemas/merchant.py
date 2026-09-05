from dataclasses import dataclass
from dataclasses_avroschema import AvroModel


@dataclass
class FakeMerchant(AvroModel):
    mer_category: str
    mer_id: str
    merchant_name: str
