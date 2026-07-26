import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import dlt
    import marimo as mo

    return alt, dlt, mo


@app.cell
def _(mo):
    mo.md("""
    # Claude Code Agent Logs Report

    Workshop data from `GET /logs`, loaded into DuckDB by the `agent_traces` dlt pipeline.
    """)
    return


@app.cell
def _(dlt):
    pipeline = dlt.attach(
        "agent_traces",
        destination="playground",
        dataset_name="traces",
    )
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT type, COUNT(*) AS records
        FROM logs
        GROUP BY 1
        ORDER BY records DESC
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1):
    _chart = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X("type:N", sort="-y", title="log type"),
        y=alt.Y("records:Q", title="records"),
        color="type:N",
        tooltip=["type:N", "records:Q"],
    ).properties(title="Logs by Type")
    _chart
    return


@app.cell
def _(dataset):
    df_chart2 = dataset("""
        SELECT DATE_TRUNC('minute', timestamp) AS minute, type, COUNT(*) AS records
        FROM logs
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2):
    _chart = alt.Chart(df_chart2).mark_line().encode(
        x=alt.X("minute:T", title="minute"),
        y=alt.Y("records:Q", title="records"),
        color="type:N",
        tooltip=["minute:T", "type:N", "records:Q"],
    ).properties(title="Log Activity per Minute by Type")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Work by git branch
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT git_branch, COUNT(*) AS records
        FROM logs
        GROUP BY 1
        ORDER BY records DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("git_branch:N", sort="-y", title="git branch"),
        y=alt.Y("records:Q", title="records"),
        color="git_branch:N",
        tooltip=["git_branch:N", "records:Q"],
    ).properties(title="Logs by Git Branch")
    _chart
    return


@app.cell
def _(dataset):
    df_chart4 = dataset("""
        SELECT git_branch, SUM(usage__output_tokens) AS output_tokens
        FROM logs
        WHERE usage__output_tokens IS NOT NULL
        GROUP BY 1
        ORDER BY output_tokens DESC
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4):
    _chart = alt.Chart(df_chart4).mark_bar().encode(
        x=alt.X("git_branch:N", sort="-y", title="git branch"),
        y=alt.Y("output_tokens:Q", title="output tokens"),
        color="git_branch:N",
        tooltip=["git_branch:N", "output_tokens:Q"],
    ).properties(title="Output Tokens by Git Branch")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Content and sessions
    """)
    return


@app.cell
def _(dataset):
    df_chart5 = dataset("""
        SELECT type, COUNT(*) AS blocks
        FROM logs__message__content
        GROUP BY 1
        ORDER BY blocks DESC
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5):
    _chart = alt.Chart(df_chart5).mark_bar().encode(
        x=alt.X("type:N", sort="-y", title="content block type"),
        y=alt.Y("blocks:Q", title="blocks"),
        color="type:N",
        tooltip=["type:N", "blocks:Q"],
    ).properties(title="Message Content Block Types")
    _chart
    return



@app.cell
def _(dataset):
    df_chart6 = dataset("""
        SELECT messages_per_session, COUNT(*) AS sessions
        FROM (
            SELECT session_id, COUNT(*) AS messages_per_session
            FROM logs
            GROUP BY 1
        )
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart6,)


@app.cell
def _(alt, df_chart6):
    _chart = alt.Chart(df_chart6).mark_bar().encode(
        x=alt.X("messages_per_session:O", title="messages per session"),
        y=alt.Y("sessions:Q", title="sessions"),
        tooltip=["messages_per_session:O", "sessions:Q"],
    ).properties(title="Distribution of Messages per Session")
    _chart
    return


if __name__ == "__main__":
    app.run()
