from decimal import Decimal
import random

from faker import Faker

from config_loader import load_config
from consts.constants import FileLocation
from data.banks_data_provider import BanksDataProvider
from data.merchants_data_provider import MerchantsDataProvider
from data.nepal_data_provider import NepalDataProvider
from data.third_party_data_provider import ThirdPartyDataProvider
from data.wallet_data_provider import WalletDataProvider
from schemas.services import P2P, MerchPay, Services, WalletLoad
from config.producer_config import (
    WalletLoadConfig,
    P2PConfig,
    MerchPayConfig,
    AmountConfig,
)

fake = Faker()
fake.add_provider(NepalDataProvider)


class ServiceBuilder:
    def build_random_service(self):
        config = load_config(config_path=FileLocation.config_file)

        service_cls = random.choice(
            [
                config.services.wallet_load,
                config.services.p2p,
                config.services.merch_pay,
            ]
        )
        class_name = service_cls.__class__
        if class_name is WalletLoadConfig:
            amount_config = config.services.wallet_load.amount
            return self.wallet_load_instance(), self._build_load_amount(amount_config)
        elif class_name is P2PConfig:
            amount_config = config.services.p2p.amount

            return self.p2p_instance(), self._build_load_amount(amount_config)
        elif class_name is MerchPayConfig:
            amount_config = config.services.merch_pay.amount
            return self.merchpay_instance(), self._build_load_amount(amount_config)

    def _build_load_amount(self, amount_config: AmountConfig) -> Decimal:
        normal_max = amount_config.normal.max
        normal_min = amount_config.normal.min
        distribution_type = amount_config.distribution.type
        if distribution_type == "uniform":
            value = random.uniform(normal_min, normal_max)
        elif distribution_type == "beta":
            alpha = amount_config.distribution.alpha
            beta = amount_config.distribution.beta
            x = random.betavariate(
                alpha=alpha,
                beta=beta,
            )
            value = round(normal_min + x * (normal_max - normal_min), 2)
        elif distribution_type == "triangular":
            value = random.triangular(
                low=normal_min,
                high=normal_max,
                mode=amount_config.distribution.mode,
            )
        else:
            raise ValueError(f"Unsupported distribution: {distribution_type}")
        return Decimal(f"{value:.2f}")

    def wallet_load_instance(self) -> WalletLoad:
        wallets = WalletDataProvider.generate_wallet_list()
        wallet = random.choice(wallets)

        return WalletLoad(
            # wallet which is being loaded by the customer
            wallet_identifier=WalletDataProvider.get_wallet_identifier(
                mobile_number=fake.phone_number()
            ),
            # wallet service provider
            wallet_provider_id=wallet.id,
            # optional third party to provide wallet services
            route_id=wallet.route_id,
        )

    def p2p_instance(self) -> P2P:
        banks = BanksDataProvider.generate_bank_list()
        bank = random.choice(banks)
        return P2P(
            bank_id=bank.id,
            route_id=bank.route_id,
            bank_acc_no=BanksDataProvider.get_bank_account(fake.phone_number()),
        )

    def merchpay_instance(self) -> MerchPay:
        merchants = MerchantsDataProvider.generate_merchants_list()
        acquirers = ThirdPartyDataProvider.get_all_third_partys()
        acquired_by = random.choice(acquirers)
        merchant = random.choice(merchants)
        return MerchPay(
            merchant_id=merchant.mer_id,
            acquirer_id=acquired_by.id,
        )
