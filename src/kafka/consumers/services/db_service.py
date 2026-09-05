from contextlib import contextmanager
from venv import logger
import psycopg2
from kafka.consumers.services.config.db_config import DBConfig
from psycopg2.extras import DictCursor


class DBService:
    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host=DBConfig.HOST,
                database=DBConfig.DATABASE,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD,
                port=DBConfig.PORT,
            )
            return conn
        except Exception as e:
            logger.error(f"DB Connection Failed {str(e)}")
            return None

    def execute_query(self, conn, query: str, values):
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, values)
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def clean_tablespace(self, conn, query: str):
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
