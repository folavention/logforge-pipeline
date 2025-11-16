# Report Generation
import sqlite3
import argparse
import json
import csv
from collections import Counter

def get_top_endpoints(cursor, limit=10):   # Retrieves the top endpoints from the logs
    cursor.execute("SELECT url FROM logs")
    urls = [row[0] for row in cursor.fetchall()]
    return Counter(urls).most_common(limit)

def get_status_code_distribution(cursor):   # Retrieves the distribution of status codes from the logs
    cursor.execute("SELECT status_code FROM logs")
    codes = [row[0] for row in cursor.fetchall()]
    return dict(Counter(codes))

def get_top_ips(cursor, limit=10):  # Retrieves the top client IPs from the logs
    cursor.execute("SELECT ip FROM logs")
    ips = [row[0] for row in cursor.fetchall()]
    return Counter(ips).most_common(limit)

def export_report(report, format="json"):  # Exports the report in the specified format (JSON or CSV)
    if format == "json":
        with open("report_summary.json", "w") as f:
            json.dump(report, f, indent=2)
        print("JSON report saved as 'report_summary.json'")
    else:
        with open("report_summary.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Section", "Data"])
            for key, value in report.items():
                writer.writerow([key, json.dumps(value)])
        print("CSV report saved as 'report_summary.csv'")

def generate_summary(format="json"):  # Generates a summary report from the logs in the database 
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    report = {
        "Top 10 Endpoints": get_top_endpoints(cursor),
        "Status Code Distribution": get_status_code_distribution(cursor),
        "Top Client IPs": get_top_ips(cursor)
    }

    export_report(report, format)
    conn.close()

def main():   # Main function to handle command line arguments and generate the report
    parser = argparse.ArgumentParser(description="Generate Apache log report summary.")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    args = parser.parse_args()

    generate_summary(args.format)      # Generate the summary report

if __name__ == "__main__":   # Entry point for the script
    main()
