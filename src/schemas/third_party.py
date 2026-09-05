from dataclasses import dataclass
from dataclasses_avroschema import AvroModel


@dataclass
class FakeThirdParty(AvroModel):
    id: str
    name: str
