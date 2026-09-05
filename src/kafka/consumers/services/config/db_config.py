import os


class DBConfig:
    """Configuration for OLAP (target) database."""

    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    DATABASE = os.getenv("POSTGRES_DB", "fraud_detection")
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
