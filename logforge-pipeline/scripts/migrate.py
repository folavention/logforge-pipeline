import psycopg2

def migrate_sqlite_to_postgres():
    # Explicit connection parameters
    pg_conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="postgres",
        host="postgres-db",   # <- important: must match the service name in docker-compose
        port="5432"
    )
    pg_cur = pg_conn.cursor()

    # Example usage (just showing, you’ll have your real migration code here)
    pg_cur.execute("SELECT 1;")
    print("Connected successfully!")

    pg_cur.close()
    pg_conn.close()


if __name__ == "__main__":
    migrate_sqlite_to_postgres()
