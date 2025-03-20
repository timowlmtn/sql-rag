import argparse
import json
import datetime
from pathlib import Path
from decimal import Decimal
from SnowflakeConnector import SnowflakeConnector
import re


class ReportProcessor:
    def __init__(self, report_folder="agent/sql/first-pass"):
        """Initialize with the report folder."""
        self.report_folder = Path(report_folder)
        self.output_base_folder = Path("data")

    def get_iso_run_date(self):
        """Return the current ISO-formatted date."""
        return datetime.date.today().isoformat()

    def read_sql_files(self, filter_pattern=None):
        """Read all SQL files in the report folder."""
        sql_files = list(self.report_folder.glob("*.sql"))
        queries = {}
        for sql_file in sql_files:
            sql_name = sql_file.stem  # Filename without extension
            if filter_pattern and not re.search(
                filter_pattern, sql_name, re.IGNORECASE
            ):
                continue  # Skip files that don't match the regex

            with open(sql_file, "r", encoding="utf-8") as file:
                queries[sql_file.stem] = file.read()
        return queries

    def process_reports(self, snowflake_conn, filter_pattern=None):
        """Execute all SQL queries and save results as JSON."""
        queries = self.read_sql_files(filter_pattern)
        iso_date = self.get_iso_run_date()
        output_folder = self.output_base_folder / iso_date
        output_folder.mkdir(parents=True, exist_ok=True)

        if not queries:
            print(f"⚠️ No SQL files matched the filter: '{filter_pattern}'")
            return

        for sql_name, query in queries.items():
            try:
                results = snowflake_conn.execute_queries(
                    query
                )  # Run each statement in order
                output_path = output_folder / f"{sql_name}.json"
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json.dump(
                        results,
                        json_file,
                        indent=4,
                        default=self.convert_to_serializable,
                    )

                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Error processing {sql_name}: {e}")

    @staticmethod
    def convert_to_serializable(obj):
        """Convert non-serializable objects (Decimal, datetime) to JSON-friendly types."""
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()  # Convert datetime to ISO string
        raise TypeError(f"Type {type(obj)} not serializable")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process SQL reports in Snowflake.")
    parser.add_argument(
        "--filter", type=str, help="Optional regex pattern to filter SQL files to run"
    )

    args = parser.parse_args()
    filter_pattern = args.filter  # Get filter pattern from arguments

    # Replace with actual Snowflake credentials
    snowflake_conn = SnowflakeConnector()

    try:
        snowflake_conn.connect()
        processor = ReportProcessor()
        processor.process_reports(snowflake_conn, filter_pattern)
    finally:
        snowflake_conn.close()
