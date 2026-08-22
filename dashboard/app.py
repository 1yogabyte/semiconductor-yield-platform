import os

import altair as alt
import streamlit as st
from google.cloud import bigquery

PROJECT_ID = "secom-yield-platform"
DATASET_ID = "secom_gold"
KEY_PATH = os.environ.get("GCP_KEY_PATH", os.path.expanduser("~/.gcp/secom-key.json"))


@st.cache_data(ttl=600)
def load_table(table_name):
    client = bigquery.Client.from_service_account_json(KEY_PATH, project=PROJECT_ID)
    return client.query(f"SELECT * FROM {DATASET_ID}.{table_name}").to_dataframe()


st.title("Semiconductor Yield Dashboard")

st.subheader("Summary")
summary = load_table("gold_summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Units", f"{int(summary['total_units'][0]):,}")
col2.metric("Yield Rate", f"{summary['yield_rate_pct'][0]:.1f}%")
col3.metric("Failed Units", int(summary['total_fail'][0]))

st.subheader("Yield by month")
yield_df = load_table("gold_yield_by_month")
st.line_chart(yield_df, x="month", y="yield_rate_pct")

st.subheader("Sensor Correlation")
corr = load_table("gold_sensor_correlation").sort_values("mean_difference", ascending=False)

chart = alt.Chart(corr).mark_bar().encode(
    x=alt.X("mean_difference:Q", title="Mean difference (pass vs fail)"),
    y=alt.Y("sensor:N", sort="-x", title="Sensor"),
)
st.altair_chart(chart, use_container_width=True)
