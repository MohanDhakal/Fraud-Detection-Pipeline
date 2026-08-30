from data.nepal_data_provider import NepalDataProvider
from schemas.third_party import FakeThirdParty
from uuid import uuid4


class ThirdPartyDataProvider:
    @staticmethod
    def get_all_third_partys() -> list[FakeThirdParty]:
        partys = NepalDataProvider.THIRD_PARTYS
        third_partys = []
        for i in partys:
            third_partys.append(FakeThirdParty(id=uuid4(), name=i))
        return third_partys
