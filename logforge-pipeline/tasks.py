from config import DB_PATH, LOG_FILE_PATH, ETL_SCRIPT_PATH
from parser import parse_log_line
from classifier import classify_logs_from_db, save_classified_logs
import os
import subprocess
import logging

def run_etl_script():       # Run the ETL script to process logs
    subprocess.run(['python', ETL_SCRIPT_PATH, LOG_FILE_PATH], check=True)

def run_classification():      
    if not os.path.exists(LOG_FILE_PATH):
        logging.warning(f"Log file not found: {LOG_FILE_PATH}")         # Log a warning if the log file does not exist
        return

    success_logs, error_logs = classify_logs_from_db(DB_PATH)   # Classify logs from the database
    save_classified_logs(success_logs, DB_PATH, 'logs_success')
    save_classified_logs(error_logs, DB_PATH, 'logs_error')
