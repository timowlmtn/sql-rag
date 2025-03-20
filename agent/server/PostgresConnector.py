import psycopg2
import os
import traceback

file_path = "/Users/timburns/PycharmProjects/OwlMountain/azrius-analytics/logs/connect.log"  # Adjust as needed


class PostgresConnector:
    connection = None

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            # Get the connection parameters from the environment
            self.connection = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "your_database"),
                user=os.getenv("POSTGRES_USER", "your_user"),
                password=os.getenv("POSTGRES_PASSWORD", "your_password"),
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432"),
            )

            table_schema = os.getenv("POSTGRES_SCHEMA", "public")

            self.connection.cursor().execute(f"SET search_path TO {table_schema};")

            return self.connection
        except psycopg2.Error as e:
            print(traceback.format_exc())
            with open(file_path, "a") as log_file:
                log_file.write(f"\nException: {e}\n")
                log_file.write(traceback.format_exc())  # Write full stack trace

            return None

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
