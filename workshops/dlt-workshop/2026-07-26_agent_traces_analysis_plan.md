# Agent traces dashboard analysis plan

## Connection

- Pipeline: `agent_traces`
- Destination: DuckDB
- Dataset: `traces`

## Profile summary

- `logs`: 20,000 rows. Key fields include `timestamp`, `type`, `git_branch`,
  `session_id`, and `usage__output_tokens`.
- `logs__message__content`: 19,668 rows. Normalized child table for message
  content blocks.
- No direct PII fields are used in the planned aggregations.

## Questions

- [x] What kinds of log events are present?
- [x] When is each event type active?
- [x] Which git branches generated the activity and output tokens?
- [x] How are message blocks and session lengths distributed?

## Data gaps

None for this report.

## Charts

The dashboard implements six aggregated Altair charts: log type counts,
activity by minute, branch counts, output-token totals by branch, content-block
types, and messages-per-session distribution.
