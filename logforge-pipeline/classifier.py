import sqlite3
import logging

def classify_logs_from_db(db_path):     # function that accepts path to sqlite
    try:
        conn = sqlite3.connect(db_path)    # connect to the sqlite database
        cursor = conn.cursor()

        # Fetch all parsed logs
        cursor.execute("SELECT * FROM logs_parsed")    # assuming logs_parsed is the table with parsed logs
        rows = cursor.fetchall()

        success_logs = []       # list to hold successful logs
        error_logs = []         # list to hold error logs

        for row in rows:                # row is a tuple representing a log entry
            log_id, ip, timestamp, method, url, protocol, status_code, size, referer, user_agent = row
            if 200 <= status_code < 400:    # classify logs based on status code
                success_logs.append(row)
            elif 400 <= status_code < 600:   # classify logs based on status code
                error_logs.append(row)

        return success_logs, error_logs

    except Exception as e:
        logging.error(f"Error classifying logs: {e}")     # log error if any
        return [], []                                       # empty lists if error occurs
    finally:
        conn.close()

def save_classified_logs(logs, db_path, table_name):         # function to save classified logs to a specified table in the database
    try:
        conn = sqlite3.connect(db_path)         # connect to the sqlite database
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                ip TEXT,
                timestamp TEXT,
                method TEXT,
                url TEXT,
                protocol TEXT,
                status_code INTEGER,
                size INTEGER,
                referer TEXT,
                user_agent TEXT
            )
        """)

        cursor.executemany(f"""                    
            INSERT INTO {table_name} (
                id, ip, timestamp, method, url, protocol,
                status_code, size, referer, user_agent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, logs)

        conn.commit()                                   # commit the changes to the database
        logging.info(f"Inserted {len(logs)} records into {table_name}")

    except Exception as e:              # log error if any
        logging.error(f"Error saving logs to {table_name}: {e}")
    finally:
        conn.close()            # close the database connection
