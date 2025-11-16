import psycopg2
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Get DB connection details from environment variables
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")  # docker service name
DB_NAME = os.getenv("POSTGRES_DB", "airflow")
DB_USER = os.getenv("POSTGRES_USER", "airflow")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def get_connection():
    """Create a database connection to PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        logging.info("Connected to PostgreSQL successfully.")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        raise

def create_tables():
    """Create the logs tables if they don't exist."""
    create_logs_table = """
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        ip TEXT NOT NULL,
        datetime TIMESTAMP NOT NULL,
        request TEXT NOT NULL,
        status_code INT NOT NULL,
        size INT,
        hash TEXT UNIQUE NOT NULL
    );
    """

    create_success_table = """
    CREATE TABLE IF NOT EXISTS logs_success (
        id SERIAL PRIMARY KEY,
        ip TEXT NOT NULL,
        datetime TIMESTAMP NOT NULL,
        request TEXT NOT NULL,
        status_code INT NOT NULL,
        size INT,
        hash TEXT UNIQUE NOT NULL
    );
    """

    create_error_table = """
    CREATE TABLE IF NOT EXISTS logs_error (
        id SERIAL PRIMARY KEY,
        ip TEXT NOT NULL,
        datetime TIMESTAMP NOT NULL,
        request TEXT NOT NULL,
        status_code INT NOT NULL,
        size INT,
        hash TEXT UNIQUE NOT NULL
    );
    """

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(create_logs_table)
        cursor.execute(create_success_table)
        cursor.execute(create_error_table)
        conn.commit()
        logging.info("Tables created or already exist.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
