# LLM Zoomcamp 2026 – dlt Workshop Homework Solution

**Author:** Venera Heddergott
**Date:** 2026-07-27

---

# Environment

```text
Python 3.13.7
dlt 1.29.1
DuckDB
Pydantic Logfire
```

The agent application was instrumented with Pydantic Logfire and generated traces after running the following query:

> How do I run Ollama locally?

---

# Question 1

## Question

For the query:

> How do I run Ollama locally?

How many spans does a single agent run produce?

## Verification

The corresponding trace was inspected in the Pydantic Logfire user interface.

## Answer

```text
5
```

---

### Question 2

### Question

How many tables did dlt create in the `agent_traces` schema?

### Verification

The `agent_traces` schema contains four tables in total:

```text
_dlt_loads
_dlt_pipeline_state
_dlt_version
spans
```

Three of these are internal metadata tables created automatically by dlt:

```text
Number of internal dlt tables: 3

_dlt_loads
_dlt_pipeline_state
_dlt_version
```

The verification command was:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'agent_traces'
  AND table_name LIKE '_dlt_%'
ORDER BY table_name;
```

Supporting evidence:

* [`q2-duckdb-tables.txt`](evidence/q2-duckdb-tables.txt)
* [`q2-dlt-internal-tables.txt`](evidence/q2-dlt-internal-tables.txt)
* [`pipeline-run.txt`](evidence/pipeline-run.txt)

### Answer

```text
3
```

This answer refers to the three internal tables automatically created by dlt. Including the loaded `spans` data table, the schema contains four tables in total.




---

# Question 3

## Question

What is the range of total input-token usage for the same agent run?

## Verification

The token usage was inspected in the corresponding Pydantic Logfire trace.

## Answer

```text
1500–5000
```

---

# Final Answers

| Question | Selected answer | Local verification               |
| -------- | --------------: | -------------------------------- |
| Q1       |           **5** | Verified in the Logfire trace    |
| Q2       |           **3** | Local pipeline produced 4 tables |
| Q3       |   **1500–5000** | Verified in the Logfire trace    |

---

# Notes

During the homework, the following issues were encountered:

* the wrong DuckDB database file was initially opened
* SQL statements were entered in zsh instead of a DuckDB or Python session
* dlt normalized nested Logfire JSON structures into additional tables
* different normalization settings produced different table structures
* the debugging expression

```python
pipeline.dataset().destination_client().config
```

raised:

```text
TypeError: 'DuckDbClient' object is not callable
```

This error occurred after the pipeline had already completed successfully.

The final pipeline run successfully fetched 16 Logfire records and loaded them into the `agent_traces` DuckDB dataset without failed jobs.
