# backup.py
import os
import shutil
import logging
from datetime import datetime, timedelta

# config
LOGS_DIR = os.getenv("LOGS_DIR", ".logs_completed")  # Directory to store completed logs
BACKUP_DIR = os.getenv("BACKUP_DIR", ".logs_backup")  # Directory to store backups
DAYS_TO_KEEP = int(os.getenv("DAYS_TO_KEEP", "30"))  # Number of days to keep logs

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_daily_folder(date: datetime) -> str:
    """Create a daily folder based on the date."""
    folder_name = date.strftime("%Y-%m-%d")
    daily_folder = os.path.join(BACKUP_DIR, folder_name)
    os.makedirs(daily_folder, exist_ok=True)
    return daily_folder

def backup_logs():
    """Backup logs from LOGS_DIR to BACKUP_DIR."""
    if not os.path.exists(LOGS_DIR):
        logging.warning(f"Logs directory '{LOGS_DIR}' does not exist.")
        return

    today = datetime.now() - timedelta(days=1)  # Backup logs from the previous day
    daily_folder = create_daily_folder(today)

    moved_files = 0
    for filename in os.listdir(LOGS_DIR):
        file_path = os.path.join(LOGS_DIR, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, daily_folder)
            logging.info(f"Copied {filename} to {daily_folder}")

        if moved_files == 0:
            logging.info(f"No files found in {LOGS_DIR} to backup.")
            return
        
        archive_path = os.path.join(daily_folder, f"{today.strftime('%Y-%m-%d')}_logs.tar.gz")
        shutil.make_archive(archive_path.replace('gztar', ''), 'gztar', daily_folder)
        logging.info(f"Archived logs to {archive_path}.tar.gz")

        cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
        for filename in os.listdir(BACKUP_DIR):
            file_path = os.path.join(BACKUP_DIR, filename)
            file_date = datetime.strptime(filename.split('_')[0], "%Y-%m-%d")
            if os.path.isdir(file_path):
                try:
                    file_date = datetime.strptime(filename, "%Y-%m-%d")
            
                    if file_date < cutoff_date:
                        shutil.rmtree(file_path)
                        logging.info(f"Deleted old backup folder: {file_path}")
                except ValueError:
                    continue  # Skip files that do not match the date format


if __name__ == "__main__":
    logging.info("Starting log backup process...")
    backup_logs()
    logging.info("Log backup process completed.")

