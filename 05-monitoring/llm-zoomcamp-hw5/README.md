# LLM Zoomcamp 2026 — Module 5: Monitoring

This folder contains my homework solution for Module 5 of the
DataTalksClub LLM Zoomcamp 2026.

The objective of this module was to add observability to a
Retrieval-Augmented Generation (RAG) pipeline using OpenTelemetry.

Instead of evaluating only the final answer, monitoring provides
visibility into how the system behaves during execution, including
latency, token usage, cost, and the runtime behavior of individual
pipeline components.

## Key Implementations

### OpenTelemetry Instrumentation

The RAG pipeline was instrumented with OpenTelemetry traces and spans.

Each RAG request produces three spans:

- `rag` — represents the complete RAG pipeline
- `search` — measures document retrieval
- `llm` — measures the language model call

The nested span structure makes it possible to understand how much time
each component contributes to the complete request.

### Runtime Metrics

The LLM span was enriched with attributes including:

- Input tokens
- Output tokens
- Estimated API cost
- Start and end times
- Span duration

These attributes provide more information than simple application logs
and can be used for performance and cost analysis.

### SQLite Trace Exporter

A custom OpenTelemetry `SQLiteSpanExporter` was implemented to persist
completed spans in a local SQLite database.

The database stores:

- Span name
- Start time
- End time
- Input tokens
- Output tokens
- Cost

Persisting the traces makes it possible to analyze system behavior
across multiple RAG executions.

### Trace Analysis

The stored trace data was loaded and analyzed using SQL and pandas.

The analysis included:

- Comparing the execution time of the `search` and `llm` spans
- Identifying the main latency bottleneck
- Examining token usage across repeated runs
- Evaluating whether the retrieved context remained stable

## Monitoring Workflow

```text
User Query
    ↓
RAG Pipeline
    ↓
Search → LLM
    ↓
OpenTelemetry Traces
    ↓
Span Attributes
    ↓
SQLite Exporter
    ↓
SQLite Database
    ↓
SQL and pandas Analysis