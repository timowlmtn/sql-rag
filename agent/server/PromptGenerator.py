import json
from datetime import datetime
from server.PostgresConnector import PostgresConnector


class PromptGenerator:
    def __init__(self, database, connection):
        """
        Initialize the class by fetching table schema details.

        :param connection: A database connection object.
        """
        self.database = database
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.schema_info = self._get_schema_info()

    def _get_schema_info(self):
        """
        Fetch all tables in the public schema along with column names and sample rows.
        """
        schema_info = {}

        # Get table names
        self.cursor.execute(
            """
            SELECT tablename FROM pg_tables WHERE schemaname = 'public';
        """
        )
        tables = [row[0] for row in self.cursor.fetchall()]

        for table in tables:
            # Get column names
            self.cursor.execute(
                f"""
                SELECT column_name FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = %s;
            """,
                (table,),
            )
            columns = [row[0] for row in self.cursor.fetchall()]

            # Get sample rows
            self.cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
            rows = self.cursor.fetchall()

            schema_info[table] = {"columns": columns, "sample_data": rows}

        return schema_info

    def generate_prompt(self, user_query):
        """
        Generate a prompt using the database schema and sample data.

        :param user_query: The user's natural language request.
        :return: A prompt string to be sent to an LLM.
        """
        schema_text = json.dumps(
            self.schema_info,
            indent=2,
            default=lambda obj: (
                obj.isoformat() if isinstance(obj, datetime) else str(obj)
            ),
        )

        prompt = f"""
        Given the following database schema and sample data:

        {schema_text}

        Generate an optimal SQL query for {self.database} to answer the following user request:
        "{user_query}"
        """

        return prompt


def main():
    # Connect to the database and generate prompts from metadata
    connector = PostgresConnector()
    connection = PromptGenerator("Postgres", connector.connect())

    if connection:
        print(
            f"✅ Prompt:\n{connection.generate_prompt('get the top 10 songs in the past week')}"
        )
    else:
        print(f"❌ Error cannot connect.")


if __name__ == "__main__":
    main()
