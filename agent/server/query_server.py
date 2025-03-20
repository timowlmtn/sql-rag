import traceback
import json
from mcp.server.fastmcp import FastMCP
from server.SingletonLogger import SingletonLogger

from PostgresConnector import PostgresConnector
from QueryHandler import QueryHandler


# Initialize FastMCP server
mcp = FastMCP("query_server")

logger = SingletonLogger("query_server").get_logger()


@mcp.tool()
async def get_query(query: str) -> str:
    """
    Runs the query
    :param query:
    :return:
    """

    try:
        logger.info(f"Running query: {query}")

        SingletonLogger("query_server").force_log(f"Running query: {query}")

        # Connect to the database
        connector = PostgresConnector()
        connection = connector.connect()

        handler = QueryHandler(connection)

        # Example SQL Execution
        result = handler.execute_query(query)

        logger.info(result["data"])

        return json.dumps(result["data"])

    except Exception as e:
        logger.error(f"\nException: {e}\n{traceback.format_exc()}")
        SingletonLogger("query_server").force_log(
            f"\nException: {e}\n{traceback.format_exc()}"
        )
        return f"⚠️ Error in call.  Check logs for details"


if __name__ == "__main__":
    logger.info(f"Running server...")

    # Initialize and run the server
    mcp.run(transport="stdio")
