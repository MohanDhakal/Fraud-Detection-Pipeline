from datetime import datetime, timedelta
from decimal import Decimal
import random
from faker.providers import BaseProvider
from enum import Enum

from schemas.location import LocationLatLong


class NetworkOperator(Enum):
    NT = "NT"
    NCELL = "NCELL"


class NepalDataProvider(BaseProvider):
    """Faker provider for Nepali Fintech context"""

    BANKS = [
        "Nabil Bank",
        "NIC Asia Bank",
        "Global IME Bank",
        "Prabhu Bank",
        "Siddhartha Bank",
        "Laxmi Sunrise Bank",
        "Everest Bank",
        "Himalayan Bank",
        "Nepal SBI Bank",
        "Standard Chartered Bank Nepal",
        "Machhapuchchhre Bank",
        "Kumari Bank",
        "NMB Bank",
        "Nepal Investment Mega Bank",
        "Sanima Bank",
        "Citizens Bank",
        "Prime Commercial Bank",
    ]
    WALLETS = [
        "eSewa",
        "Khalti by IME",
        "NamastePay",
        "CellPay",
        "MoRu",
        "QPay",
    ]
    MERCHANTS = {
        "GROCERY": [
            "Bhatbhateni Supermarket",
            "BigMart",
            "Salesberry",
        ],
        "RESTAURANT": [
            "Bajeko Sekuwa",
            "Roadhouse Cafe",
            "Fire and Ice Pizzeria",
            "Nanglo Bakery Cafe",
            "Jimbu Thakali",
            "Himalayan Java",
            "Chick n Chill",
        ],
        "E-COMMERCE": [
            "Daraz Nepal",
            "SastoDeal",
            "Thulo.com",
            "Foodmandu",
        ],
        "UTILITY": [
            "Nepal Electricity Authority",
            "Nepal Telecom",
            "Ncell",
            "Khanepani (Kathmandu Upatyaka)",
            "Worldlink",
            "DishHome",
        ],
        "REMIT": [
            "IME Remit",
            "Western Union Nepal",
            "MoneyGram (City Express)",
            "Prabhu Money Transfer",
            "Muktinath Remit",
        ],
        "TRAVEL": [
            "Yeti Airlines",
            "Buddha Air",
            "Sajha Yatayat",
            "InDrive",
            "Pathao Nepal",
        ],
        "EDUCATION": [
            "Kathmandu University",
            "Tribhuvan University",
            "Pokhara University",
            "British College",
        ],
        "HEALTH": [
            "Patan Hospital",
            "Mediciti Hospital",
            "Grande International Hospital",
            "Nepal Mediciti",
            "Dhulikhel Hospital",
        ],
    }
    DISTRICTS = [
        ("Kathmandu", 27.7172, 85.3240),
        ("Lalitpur", 27.6667, 85.3167),
        ("Bhaktapur", 27.6710, 85.4278),
        ("Pokhara (Kaski)", 28.2096, 83.9856),
        ("Chitwan (Bharatpur)", 27.6833, 84.4333),
        ("Biratnagar (Morang)", 26.4542, 87.2794),
        ("Birgunj (Parsa)", 27.0000, 84.8667),
        ("Butwal (Rupandehi)", 27.7000, 83.4500),
        ("Dharan (Sunsari)", 26.8167, 87.2833),
        ("Janakpur (Dhanusa)", 26.7286, 85.9260),
        ("Nepalgunj (Banke)", 28.0500, 81.6167),
        ("Hetauda (Makwanpur)", 27.4167, 85.0333),
        ("Dhangadhi (Kailali)", 28.7000, 80.5833),
        ("Mahendranagar (Kanchanpur)", 28.9167, 80.3333),
        ("Itahari (Sunsari)", 26.6667, 87.2833),
        ("Banepa (Kavrepalanchok)", 27.6333, 85.5167),
    ]
    NEPALI_FULL_NAMES = [
        "Aarav Sharma",
        "Aayush Adhikari",
        "Amit Shrestha",
        "Anil Koirala",
        "Anish Bhandari",
        "Arjun Poudel",
        "Ashish Gautam",
        "Bibek Acharya",
        "Bikash Bhattarai",
        "Binod Dahal",
        "Bipin Aryal",
        "Bishal KC",
        "Chandan Regmi",
        "Deepak Nepal",
        "Dhiraj Ghimire",
        "Dipesh Subedi",
        "Gaurav Sigdel",
        "Hari Prasad Dhakal",
        "Hemant Rijal",
        "Ishan Neupane",
        "Kamal Karki",
        "Kiran Sapkota",
        "Krishna Joshi",
        "Madan Parajuli",
        "Mahesh Kafle",
        "Manish Tiwari",
        "Nabin Pandey",
        "Niraj Kharel",
        "Nischal Lamsal",
        "Prabin Oli",
        "Pradeep Basnet",
        "Prakash Baral",
        "Prashant Kandel",
        "Rabin Panta",
        "Rajan Pokharel",
        "Rajesh Thapa",
        "Ramesh Khadka",
        "Roshan Acharya",
        "Sagar Bista",
        "Santosh Dhungana",
        "Saroj Mainali",
        "Shyam Adhikari",
        "Sudip Koirala",
        "Sujan Sharma",
        "Suman Poudel",
        "Sunil Bhandari",
        "Suraj Gautam",
        "Suresh Aryal",
        "Tek Bahadur Magar",
        "Ujjwal Rai",
        "Aakriti Shrestha",
        "Alisha Koirala",
        "Anjana Adhikari",
        "Anusha Poudel",
        "Asmita Gautam",
        "Asha Sharma",
        "Barsha Acharya",
        "Bimala Karki",
        "Bina Dahal",
        "Deepa Bhattarai",
        "Dikshya Nepal",
        "Ganga KC",
        "Gita Aryal",
        "Ishwori Regmi",
        "Jenisha Subedi",
        "Kabita Ghimire",
        "Karuna Pandey",
        "Laxmi Joshi",
        "Manju Kafle",
        "Menuka Sapkota",
        "Nikita Neupane",
        "Nirmala Oli",
        "Nisha Basnet",
        "Pabitra Dhakal",
        "Prabha Baral",
        "Pramila Tiwari",
        "Pratima Kharel",
        "Puja Pokharel",
        "Rachana Panta",
        "Rekha Thapa",
        "Renuka Mainali",
        "Rita Sigdel",
        "Sabina Lamsal",
        "Sabitri Parajuli",
        "Samikshya Adhikari",
        "Sangita Kandel",
        "Saraswati Acharya",
        "Sarita Sharma",
        "Sharmila Poudel",
        "Shristi Gautam",
        "Smriti Bhattarai",
        "Sneha Dahal",
        "Srijana Karki",
        "Sudha Aryal",
        "Sunita Nepal",
        "Susan Koirala",
        "Sushma Regmi",
        "Tara Ghimire",
        "Urmila Pandey",
        "Yamuna Joshi",
        "Yashoda Basnet",
        "Zenisha Khadka",
    ]
    MOBILE_PREFIXES = {
        "NT": ["984", "985", "986", "974", "976"],
        "NCELL": ["980", "981", "982", "970", "971"],
    }
    THIRD_PARTYS = ["FONEPAY", "NPS", "NCHL", "SCT"]

    def bank_name(self) -> str:
        return self.random_element(self.BANKS)

    def wallet_name(self) -> str:
        return self.random_element(self.WALLETS)

    def merchant_name(self, category: str = None) -> str:
        """Return a merchant name. If category is None, pick a random category first."""
        if category is None:
            category = self.random_element(list(self.MERCHANTS.keys()))
        return self.random_element(self.MERCHANTS[category])

    def merchant_category(self) -> str:
        return self.random_element(list(self.MERCHANTS.keys()))

    def district(self) -> str:
        return self.random_element(self.DISTRICTS)[0]

    def location(self) -> LocationLatLong:
        city, lat, long = self.random_element(self.DISTRICTS)
        return LocationLatLong(
            name=city, lat=Decimal(str(lat)), long=Decimal(str(long))
        )

    def mobile_number(self, operator: str = None) -> str:
        # if none specified consider it as a NT Operator
        if operator is None:
            operator = self.random_element(list(self.MOBILE_PREFIXES.keys()))

        suffix = "".join([str(random.randint(0, 9)) for _ in range(7)])
        prefix = self.random_element(self.MOBILE_PREFIXES[operator])
        return f"{prefix}{suffix}"

    def name(self):
        name = self.random_element(self.NEPALI_FULL_NAMES)
        return name

    def phone_number(
        self,
        network_operator: NetworkOperator = None,
    ) -> str:
        if network_operator is None:
            return self.mobile_number()
        return self.mobile_number(operator=network_operator.name)

    def bank_account_number(self, bank_name: str = None) -> str:
        length = self.random_int(min=10, max=14)
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    def wallet_id(self, wallet_name: str = None) -> str:
        return self.mobile_number()

    def datetime(self) -> datetime:
        """Generate a random datetime between start and end."""
        start = datetime(2020, 1, 1)
        end = datetime.now()
        if start >= end:
            raise ValueError("start must be before end")

        delta_seconds = int((end - start).total_seconds())
        random_seconds = random.randint(0, delta_seconds)

        return start + timedelta(seconds=random_seconds)
