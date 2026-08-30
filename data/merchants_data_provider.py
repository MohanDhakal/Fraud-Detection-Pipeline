from unicodedata import category
from uuid import uuid4
from data.nepal_data_provider import NepalDataProvider
from schemas.merchant import FakeMerchant


class MerchantsDataProvider:
    @staticmethod
    def generate_merchants_list() -> list[FakeMerchant]:
        fake_merchant_list = []
        merchants_categorized = NepalDataProvider.MERCHANTS.items()
        for category, merchants in merchants_categorized:
            for merchant_name in merchants:
                fake_merchant_list.append(
                    FakeMerchant(
                        mer_id=uuid4(),
                        mer_category=category,
                        merchant_name=merchant_name,
                    ),
                )

        return fake_merchant_list
