import os
import psycopg2
from contextlib import contextmanager

DATABASE_URL = f"dbname={os.getenv('POSTGRES_DB')} user={os.getenv('POSTGRES_USER')} password={os.getenv('POSTGRES_PASSWORD')} host={os.getenv('POSTGRES_HOST')} port={os.getenv('POSTGRES_PORT')}"

@contextmanager
def get_db_cursor():
    """
    Dependency untuk menyediakan cursor database per-request dan menangani transaksi.
    """
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Database transaction failed: {e}")
        raise
    finally:
        conn.close()