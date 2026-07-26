"""Load Claude Code agent logs from the workshop REST API into DuckDB.

The API is public and exposes GET /logs.  It returns an envelope with a
``logs`` array and a ``total`` record count, using ``limit``/``offset``
pagination.

Run ``uv run python rest_api_pipeline.py`` to load the workshop sample of
20,000 records.  Pass ``--full`` to load all available records.
"""

import sys
from typing import Any

import dlt
from dlt.hub import run
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

BASE_URL = "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app"
PAGE_SIZE = 1_000
SAMPLE_PAGES = 20


@dlt.source(name="agent_logs_api")
def agent_logs_source(
    base_url: str = dlt.config.value, page_size: int = PAGE_SIZE
) -> Any:
    """Create the REST API source for Claude Code agent logs.

    Args:
        base_url: API base URL, configurable via ``[sources.agent_logs_api]``.
        page_size: Number of logs requested in each API page.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "paginator": {
                "type": "offset",
                "limit": page_size,
                "offset": 0,
                "limit_param": "limit",
                "offset_param": "offset",
                "total_path": "total",
            },
        },
        "resource_defaults": {"write_disposition": "replace"},
        "resources": [
            {
                "name": "logs",
                "primary_key": "index",
                "endpoint": {"path": "/logs", "data_selector": "logs"},
            }
        ],
    }
    yield from rest_api_resources(config)


@run.pipeline("agent_traces")
def load(full: bool = False) -> None:
    """Load 20,000 records by default, or every record with ``full=True``."""
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces",
        destination="playground",
        dataset_name="traces",
    )
    source = agent_logs_source(base_url=BASE_URL)
    if not full:
        source.add_limit(SAMPLE_PAGES)

    load_info = pipeline.run(source)
    print(load_info)


if __name__ == "__main__":
    load(full="--full" in sys.argv)
