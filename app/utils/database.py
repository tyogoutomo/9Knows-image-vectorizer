import os
import psycopg2
import time
import logging

# Global database connection
_db_connection = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_db_connection(max_retries=5, retry_delay=2):
    """Initialize the database connection with retry logic."""
    global _db_connection
    if _db_connection is not None and not _db_connection.closed:
        return
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")
            _db_connection = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT")
            )
            _db_connection.autocommit = False
            logger.info("Database connection initialized successfully.")
            return
        except psycopg2.OperationalError as e:
            logger.warning(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to database after all retries")
                raise

def get_db_connection():
    """Get the database connection, reconnecting if needed."""
    global _db_connection
    if _db_connection is None or _db_connection.closed:
        initialize_db_connection()
    return _db_connection

def clear_table():
    """Delete all records from the image_vectors table."""
    try:
        cursor = get_db_connection().cursor()
        cursor.execute("DELETE FROM image_vectors")
        get_db_connection().commit()
        cursor.close()
        logger.info("All records deleted from image_vectors table")
    except Exception as e:
        logger.error(f"Error clearing table: {e}")
        raise