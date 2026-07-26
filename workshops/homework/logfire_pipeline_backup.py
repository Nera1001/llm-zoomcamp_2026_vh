"""
Load Logfire traces into DuckDB using dlt.
"""

import os

import dlt
from dotenv import load_dotenv
from logfire.experimental.query_client import LogfireQueryClient


load_dotenv()

READ_TOKEN = os.getenv("LOGFIRE_READ_TOKEN")

if not READ_TOKEN:
    raise ValueError(
        "LOGFIRE_READ_TOKEN is missing. "
        "Add it to the .env file."
    )


@dlt.resource(
    name="spans",
    write_disposition="replace",
)
def logfire_spans():
    """
    Fetch Logfire records and yield them to dlt.

    The complete attributes object is retained so dlt can normalize
    nested LLM messages, tool calls and token-usage structures.
    """
    sql = """
    SELECT *
    FROM records
    ORDER BY start_timestamp DESC
    LIMIT 1000
    """

    with LogfireQueryClient(read_token=READ_TOKEN) as client:
        rows = client.query_json_rows(sql=sql)

    if isinstance(rows, dict):
        # Defensive handling in case the client wraps the result.
        rows = rows.get("rows") or rows.get("data") or [rows]

    if not rows:
        print("No Logfire records were returned.")
        return

    print(f"Fetched {len(rows)} Logfire records.")

    yield from rows


def run_pipeline() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination=dlt.destinations.duckdb(
            credentials="logfire_traces.duckdb"
        ),
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(logfire_spans())

    print(load_info)
    print(f"Database: {pipeline.dataset().destination_client().config}")


if __name__ == "__main__":
    run_pipeline()