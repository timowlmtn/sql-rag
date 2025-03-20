from typing import Any, Dict, Union


class QueryHandler:
    default_query = """
SELECT airdate,
       album,
       artist,
       song,
       program_name,
       program_tags,
       host_names,
       release_date
FROM import_kexp_playlist
ORDER BY airdate DESC
LIMIT 20
    """

    def __init__(self, connection):
        """
        Initializes the QueryHandler with an SQLite database connection.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def execute_query(
        self, query: str, params: Union[tuple, Dict[str, Any]] = ()
    ) -> Dict[str, Any]:
        """
        Executes an SQL query and returns the results.
        """
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()
