import random

from builders.service_builder import ServiceBuilder
from data.nepal_data_provider import NepalDataProvider
from schemas.customer import Customer
from schemas.transaction import Transaction
from faker import Faker
from datetime import datetime

fake = Faker()
fake.add_provider(NepalDataProvider)


class TransactionBuilder:

    def build_normal_transaction(
        self,
        customers_pool: list[Customer],
    ) -> Transaction | None:
        transaction_id = fake.uuid4()
        # transactions should be from start_date to the current local datetime
        transaction_datetime = fake.date_time_between(
            start_date=datetime(2021, 7, 12, 0, 0, 0),
            end_date=datetime.now(),
        )
        currency = "NPR"
        # select a random customer making a transaction
        customer = random.choice(customers_pool)
        # build service and amount for it
        service_builder = ServiceBuilder()
        if service_builder.build_random_service() is not None:
            service, amount = service_builder.build_random_service()
            transaction = Transaction(
                id=transaction_id,
                customer=customer,
                amount=amount,
                timestamp=transaction_datetime,
                location=customer.location,
                ip_address=customer.usual_ip,
                currency=currency,
                service_obj=service,
                device_id=customer.device_id,
            )
            return transaction
        else:
            print("Cannot  build transaction without a service")
