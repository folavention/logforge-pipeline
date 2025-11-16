import re
import hashlib
from datetime import datetime
import logging
import os

# Setup basic logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log_parser.log"),
        logging.StreamHandler()
    ]
)

# Apache log pattern
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - '
    r'\[(?P<datetime>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<url>\S+) HTTP/(?P<protocol_version>\d\.\d)" '
    r'(?P<status>\d{3}) '
    r'(?P<size>\d+|-) '
    r'"(?P<referer>[^"]*)" '
    r'"(?P<user_agent>[^"]*)"'
)

def parse_log_line(line):
    """Parses a single line of Apache log and returns a dictionary of parsed fields."""
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def generate_log_hash(ip, datetime_str, url):
    """Generates a unique hash for the log entry based on IP, datetime, and URL."""
    hash_input = ip + datetime_str + url
    return hashlib.sha256(hash_input.encode()).hexdigest()

def transform(lines):
    """Transforms raw log lines into structured logs."""
    parsed_logs = []
    errors = []
    seen_hashes = set()

    logging.info("Starting transformation of log lines.")
    logging.info(f"Total lines received: {len(lines)}")

    for idx, line in enumerate(lines, start=1):
        try:
            parsed = parse_log_line(line)
            if not parsed:
                logging.warning(f"Line {idx} could not be parsed.")
                errors.append((line.strip(), "Parsing returned None"))
                continue

            # Convert timestamp to ISO format
            try:
                parsed["datetime"] = datetime.strptime(
                    parsed["datetime"], "%d/%b/%Y:%H:%M:%S %z"
                ).isoformat()
            except Exception:
                logging.warning(f"Line {idx} has invalid timestamp.")
                errors.append((line.strip(), "Invalid timestamp format"))
                continue

            # Convert status code to integer
            try:
                parsed["status_code"] = int(parsed["status"])
            except Exception:
                logging.warning(f"Line {idx} has invalid status code.")
                errors.append((line.strip(), "Invalid status code"))
                continue

            # Convert size to integer, default to 0
            size_value = parsed.get("size", "0")
            parsed["size"] = int(size_value) if size_value.isdigit() else 0

            # Deduplication
            record_hash = generate_log_hash(parsed["ip"], parsed["datetime"], parsed["url"])
            if record_hash in seen_hashes:
                logging.debug(f"Line {idx} is a duplicate. Skipping.")
                continue
            seen_hashes.add(record_hash)

            # Prepare clean log dict
            clean_log = {
                "ip": parsed["ip"],
                "datetime": parsed["datetime"],
                "method": parsed["method"],
                "url": parsed["url"],
                "status_code": parsed["status_code"],
                "size": parsed["size"],
                "referrer": parsed["referer"],
                "user_agent": parsed["user_agent"]
            }

            parsed_logs.append(clean_log)

        except Exception as e:
            logging.error(f"Unexpected error at line {idx}: {e}")
            errors.append((line.strip(), str(e)))

    logging.info(f"Parsing completed. Parsed: {len(parsed_logs)} | Errors: {len(errors)}")
    return parsed_logs, errors
