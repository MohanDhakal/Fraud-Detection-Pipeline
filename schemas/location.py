from dataclasses import dataclass
from dataclasses_avroschema import AvroModel, types


@dataclass
class LocationLatLong(AvroModel):
    name: str
    lat: types.condecimal(
        max_digits=9,
        decimal_places=6,
    )  # type: ignore
    long: types.condecimal(
        max_digits=9,
        decimal_places=6,
    )  # type: ignore
