# extractor.py

import os
import logging
import requests
from time import sleep

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")       # Configure logging format

# Default API endpoint (can be overridden with env variable)
API_URL = os.getenv("LOG_API_URL", "https://apache-api.onrender.com/logs")          # Default API URL
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))                  # Maximum number of retries for API requests
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))  # seconds

def fetch_logs_from_api():     # Function to fetch logs from the API
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            logging.info(f"Attempt {attempt+1} to fetch logs from {API_URL}")       # Log the attempt number
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()

            logs = response.text.strip().splitlines()       # Split the response text into lines
            logging.info(f"Successfully fetched {len(logs)} log lines.")
            return logs

        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed: {e}")
            attempt += 1
            if attempt < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                sleep(RETRY_DELAY)
            else:
                logging.error("Max retries exceeded. Failed to fetch logs.")
                raise RuntimeError("Log fetching failed after retries.")

if __name__ == "__main__":          # Main block to run the extractor
    try:
        log_lines = fetch_logs_from_api()
        for line in log_lines[:5]:  # Preview first 5 lines
            print(line)
    except Exception as e:
        logging.error(f"Extractor failed: {e}")
