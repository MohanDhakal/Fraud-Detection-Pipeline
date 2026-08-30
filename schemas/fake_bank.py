from dataclasses import dataclass
from dataclasses_avroschema import AvroModel


@dataclass
class FakeBank(AvroModel):
    id: str
    name: str
    route_id: str = None
