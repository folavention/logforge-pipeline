import argparse
import logging
import os
from parser import transform
from database import create_table, insert_logs

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === Environment Config ===
DEFAULT_DB_PATH = os.getenv("LOG_DB_PATH", "logs.db")

def process_logs(file_path):  # Process log file with transform() and insert into DB
    logging.info(f"Checking file: {file_path}")
    if not os.path.exists(file_path):
        logging.error(f"Log file does not exist: {file_path}")
        return

    create_table()

    with open(file_path, "r") as f:
        lines = f.readlines()

    parsed_logs, errors = transform(lines)

    if parsed_logs:
        insert_logs(parsed_logs)

    logging.info(f"Done. Total: {len(lines)}, Inserted: {len(parsed_logs)}, Failed: {len(errors)}")

def main():
    parser = argparse.ArgumentParser(description="Process Apache log file into SQLite DB.")
    parser.add_argument("file", help="Path to the Apache log file")
    args = parser.parse_args()

    process_logs(args.file)

if __name__ == "__main__":
    main()
