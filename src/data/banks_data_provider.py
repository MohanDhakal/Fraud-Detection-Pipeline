from uuid import uuid4
from data.nepal_data_provider import NepalDataProvider
from data.third_party_data_provider import ThirdPartyDataProvider
from schemas.fake_bank import FakeBank
import random


class BanksDataProvider:

    @staticmethod
    def generate_bank_list() -> list[FakeBank]:
        fb_list = []
        banks = NepalDataProvider.BANKS
        routes = ThirdPartyDataProvider.get_all_third_partys()

        for bank in banks:
            route = random.choice(routes)
            fb_list.append(
                FakeBank(
                    id=uuid4(),
                    name=bank,
                    route_id=route.id,
                )
            )
        return fb_list

    @staticmethod
    def get_bank_account(mobile_number: str) -> str:
        bank_list = BanksDataProvider.generate_bank_list()
        bank = random.choice(bank_list)
        # count number of character in bank name
        char_count = len(bank.name)
        # find a random 3 digit number, x controls the seed, for consistent random number generation
        rng = random.Random(x=len(bank.name))
        three_digit = rng.randint(100, 999)
        # first 2 character from the bank name
        prefix = bank.name.strip()[:2]
        return f"{prefix.upper()}{char_count}{mobile_number}{three_digit}"
