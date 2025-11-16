import sqlite3
import psycopg2
import hashlib

# SQLite config
SQLITE_DB_PATH = "etl_pipeline.db"

# PostgreSQL config
PG_CONFIG = {
    "dbname": "logsdb",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

TABLES = ["logs_success", "logs_error"]

def get_sqlite_stats(table):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM {table}")
    count, min_ts, max_ts = cursor.fetchone()

    cursor.execute(f"SELECT GROUP_CONCAT(SHA256_HASH) FROM {table}")
    hash_concat = cursor.fetchone()[0] or ""
    hash_total = hashlib.sha256(hash_concat.encode()).hexdigest() if hash_concat else None

    conn.close()
    return count, min_ts, max_ts, hash_total

def get_postgres_stats(table):
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM {table}")
    count, min_ts, max_ts = cursor.fetchone()

    cursor.execute(f"SELECT STRING_AGG(sha256_hash, '') FROM {table}")
    hash_concat = cursor.fetchone()[0] or ""
    hash_total = hashlib.sha256(hash_concat.encode()).hexdigest() if hash_concat else None

    conn.close()
    return count, min_ts, max_ts, hash_total

if __name__ == "__main__":
    print("=== Migration Verification ===\n")

    for table in TABLES:
        print(f"Checking table: {table}")

        sqlite_count, sqlite_min, sqlite_max, sqlite_hash = get_sqlite_stats(table)
        pg_count, pg_min, pg_max, pg_hash = get_postgres_stats(table)

        print(f"  SQLite - Rows: {sqlite_count}, Range: {sqlite_min} → {sqlite_max}, Hash: {sqlite_hash}")
        print(f"  Postgres - Rows: {pg_count}, Range: {pg_min} → {pg_max}, Hash: {pg_hash}")

        if (sqlite_count == pg_count) and (sqlite_hash == pg_hash):
            print("Match confirmed")
        else:
            print("Mismatch detected")

        print("-" * 40)
