import yaml
from config.consumer_config import ConsumerConfig
from config.producer_config import ProducerConfig


def load_config(config_path: str) -> ProducerConfig:
    with open(config_path) as cf:
        data = yaml.safe_load(cf)
    config = ProducerConfig(**data)
    return config


def load_consumer_config(config_path: str) -> ConsumerConfig:
    with open(config_path) as cf:
        data = yaml.safe_load(cf)
    config = ConsumerConfig(**data)
    return config
