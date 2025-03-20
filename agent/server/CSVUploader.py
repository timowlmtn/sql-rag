import traceback

import pandas as pd
import psycopg2
import argparse
from PostgresConnector import PostgresConnector
import os


class CSVUploader:
    def __init__(self, connection):
        self.connection = connection

    def create_table_from_csv(self, file_path):
        """Creates a table based on the CSV file's first row (column names)."""
        table_name = os.path.splitext(os.path.basename(file_path))[0].upper()
        df = pd.read_csv(file_path)

        # Get column names and types (assuming text type for simplicity)
        columns = df.columns
        columns_type = []
        for column in columns:
            if column == "AIRDATE":
                columns_type.append(f"{column} TIMESTAMP")
            elif column == "RELEASE_DATE":
                columns_type.append(f"{column} TEXT")
            else:
                columns_type.append(f"{column} TEXT")

        column_definitions = ", ".join(columns_type)

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});
        """

        print(create_table_query)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
                self.connection.commit()
                print(f"Table '{table_name}' created or already exists.")
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
            self.connection.rollback()

        return table_name

    def upload_csv(self, file_path):
        """Uploads the CSV file to the corresponding table only if AIRDATE is greater than the max airdate."""
        table_name = self.create_table_from_csv(file_path)
        df = pd.read_csv(
            file_path,
            dtype=str,
            parse_dates=["AIRDATE"],
            date_format="%Y-%m-%d %H:%M:%S",
        )

        # Get max AIRDATE from the existing table
        max_airdate_query = f"SELECT MAX(airdate) FROM {table_name}"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(max_airdate_query)
                max_airdate = cursor.fetchone()[0]  # Get the max AIRDATE

                if max_airdate is None:
                    print(f"No existing data in {table_name}, inserting all rows.")
                else:
                    print(f"Max airdate in table: {max_airdate}")

                # Filter rows where AIRDATE is greater than the max_airdate
                if max_airdate is not None:
                    max_airdate = pd.to_datetime(
                        max_airdate
                    )  # Convert string to Timestamp

                    # Convert DataFrame AIRDATE column to datetime for proper comparison
                    df["AIRDATE"] = pd.to_datetime(df["AIRDATE"], errors="coerce")

                    existing = df["AIRDATE"]
                    print(f"Filtering airdate {existing} to {max_airdate}")
                    df = df[df["AIRDATE"] > max_airdate]

                if df.empty:
                    print("No new records to insert.")
                    return

                # Prepare the INSERT statement
                placeholders = ", ".join(["%s"] * len(df.columns))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

                # Insert only the filtered rows
                for row in df.itertuples(index=False, name=None):
                    cursor.execute(insert_query, row)

                self.connection.commit()
                print(f"Inserted {len(df)} new rows into '{table_name}'.")

        except psycopg2.Error as e:
            print(f"Error inserting data: {e}\n{traceback.format_exc()}")
            self.connection.rollback()


def main():
    # Parse command-line arguments for the CSV file path
    parser = argparse.ArgumentParser(description="Upload a CSV file to PostgreSQL.")
    parser.add_argument("csv_file", help="Path to the CSV file to upload")
    args = parser.parse_args()

    csv_file_path = args.csv_file

    # Connect to the database
    connector = PostgresConnector()
    connection = connector.connect()

    if connection:
        uploader = CSVUploader(connection)
        uploader.upload_csv(csv_file_path)
        connector.close()
    else:
        print(f"❌ Error cannot connect.")


if __name__ == "__main__":
    main()
