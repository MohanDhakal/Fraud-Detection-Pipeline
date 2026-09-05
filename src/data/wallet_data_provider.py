import random
from typing import Counter

from data.nepal_data_provider import NepalDataProvider
from data.third_party_data_provider import ThirdPartyDataProvider
from schemas.fake_wallet import FakeWallet
from uuid import uuid4


class WalletDataProvider:
    @staticmethod
    def generate_wallet_list() -> list[FakeWallet]:
        wallets = NepalDataProvider.WALLETS
        wallet_list = []
        routes = ThirdPartyDataProvider.get_all_third_partys()
        for wallet in wallets:
            route = random.choice(routes)
            wallet_list.append(
                FakeWallet(
                    name=wallet,
                    id=uuid4(),
                    route_id=route.id,
                ),
            )
        return wallet_list

    @staticmethod
    def get_wallet_identifier(mobile_number: str) -> str:
        wallet_list = WalletDataProvider.generate_wallet_list()
        wallet = random.choice(wallet_list)
        # count number of character in wallet name
        char_count = len(wallet.name)
        # find a random 3 digit number, x controls the seed, for consistent random number generation
        rng = random.Random(x=len(wallet.name))
        three_digit = rng.randint(100, 999)
        # first 2 character from the bank name
        prefix = wallet.name.strip()[:2]
        return f"{prefix.upper()}{char_count}{mobile_number}{three_digit}"
