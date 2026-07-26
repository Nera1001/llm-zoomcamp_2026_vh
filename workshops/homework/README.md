# dltHub Workshop – Claude Code Agent Logs Dashboard

This project was created as part of the **dltHub Workshop** from the **LLM Zoomcamp 2026**.

It demonstrates how to build an end-to-end data pipeline using **dlt**, deploy it to **dltHub Cloud**, and visualize the data with a **Marimo dashboard**.

---

# Architecture

```
REST API
    │
    ▼
dlt REST Source
    │
    ▼
dlt Pipeline
    │
    ▼
Playground Dataset (traces)
    │
    ▼
Marimo Dashboard
    │
    ▼
dltHub Cloud Deployment
```

---

# Features

- Extracts agent logs from a REST API
- Loads data with dlt
- Stores data in the dltHub Playground destination
- Creates a dataset named `traces`
- Interactive Marimo dashboard
- Cloud deployment with dltHub
- Public dashboard sharing
- Job monitoring through dltHub

---

# Project Structure

```
.
├── agent_traces_dashboard.py
├── rest_api_pipeline.py
├── __deployment__.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

# Technologies

- Python
- dlt
- dltHub
- Marimo
- Altair
- Pandas
- UV

---

# Deployment

Deploy the project

```bash
uv run dlthub deploy
```

Run the pipeline

```bash
uv run dlthub run load
```

Open the workspace

```bash
uv run dlthub show
```

Publish the dashboard

```bash
uv run dlthub job publish agent_traces_dashboard
```

---

# Dashboard

The dashboard connects directly to the deployed Playground dataset.

```python
pipeline = dlt.attach(
    "agent_traces",
    destination="playground",
    dataset_name="traces",
)
```

---

# Dataset

Pipeline

```
agent_traces
```

Dataset

```
traces
```

Destination

```
playground
```

---

# What I Learned

During this workshop I learned how to:

- Build REST API pipelines with dlt
- Create reusable data ingestion pipelines
- Deploy pipelines to dltHub Cloud
- Store data in the Playground destination
- Build interactive dashboards using Marimo
- Publish dashboards
- Monitor cloud jobs
- Troubleshoot deployment and dependency issues

---

# Result

Successfully deployed:

- REST API pipeline
- Playground dataset
- Interactive Marimo dashboard
- Public dashboard
- Cloud job monitoring

---

# Acknowledgements

This project was completed as part of the **LLM Zoomcamp 2026** and the **dltHub Workshop**.

Special thanks to:

- Alexey Grigorev
- DataTalks.Club
- dltHub