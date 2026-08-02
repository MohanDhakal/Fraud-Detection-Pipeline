import random
from consts.constants import FileLocation
from data.banks_data_provider import BanksDataProvider
from data.nepal_data_provider import NepalDataProvider
from data.wallet_data_provider import WalletDataProvider
from schemas.customer import Customer
from config_loader import load_config
from faker import Faker
import random

fake = Faker()
fake.add_provider(NepalDataProvider)


class CustomerBuilder:

    def build_customers(self) -> list[Customer]:
        config = load_config(FileLocation.config_file)
        count = config.customers.count
        customers = []
        for i in range(count):
            full_name = fake.name()
            user_name = f"{full_name.replace(" ","").lower()}.{i}"
            email = f"{user_name}{random.choice(['@gmail.com','@yahoo.com','@outlook.com'])}"
            fake_location = fake.location()
            phone_number = fake.phone_number()
            customer_id = fake.uuid4()
            created_datetime = fake.datetime()
            device_id = fake.uuid4()
            ip_address = fake.ipv4()
            bank = fake.bank()
            wallets = WalletDataProvider.generate_wallet_list()
            # wallet = random.choice(wallets)
            banks = BanksDataProvider.generate_bank_list()
            # bank = random.choice(banks)
            customers.append(
                Customer(
                    id=customer_id,
                    name=full_name,
                    email=email,
                    msisdn=phone_number,
                    created_on=created_datetime,
                    device_id=device_id,
                    location=fake_location,
                    wallet_id=WalletDataProvider.get_wallet_identifier(
                        mobile_number=phone_number
                    ),
                    bank_acc_no=BanksDataProvider.get_bank_account(
                        mobile_number=phone_number
                    ),
                    usual_ip=ip_address,
                    # bank=bank,
                    # wallet=wallet,
                ),
            )
        return customers
