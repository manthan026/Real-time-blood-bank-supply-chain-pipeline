import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="Blood Bank Supply Chain Dashboard",
    page_icon="🩸",
    layout="wide"
)

# Ensure dashboard directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from db import load_data, get_db_status


def load_css():
    css_path = os.path.join(current_dir, "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(current_dir, "dashboard", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# Auto Refresh every 1 minute
st_autorefresh(
    interval=60000,   # 60 seconds
    key="refresh"
)

# Dashboard Header
st.markdown("""
<div style='
    background: linear-gradient(90deg, #b71c1c, #e53935);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    box-shadow: 0 4px 15px rgba(183, 28, 28, 0.3);
'>

<h1 style='color:white; margin-bottom:5px; font-weight:800; font-size:2rem;'>
🩸 Blood Bank Supply Chain Management Dashboard
</h1>

<p style='font-size:16px; margin-top:0; opacity: 0.95;'>
Real-Time Monitoring • Kafka • Spark Structured Streaming • AWS RDS • Streamlit
</p>

</div>
""", unsafe_allow_html=True)

# Connection & Refresh Banner
is_live_db, db_message = get_db_status()
status_badge_color = "#2e7d32" if is_live_db else "#e65100"
status_badge_text = "🟢 MySQL Database Active" if is_live_db else "⚡ Live Simulation Stream"

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:10px 5px;
        font-size:14px;
        color:#444;
        flex-wrap: wrap;
        gap: 10px;
    ">
        <span>🔄 Last Refreshed: <b>{datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}</b></span>
        <span style="background:{status_badge_color}15; color:{status_badge_color}; padding:4px 12px; border-radius:20px; font-weight:600; border:1px solid {status_badge_color}40;">{status_badge_text}</span>
        <span>⏱ Auto Refresh: <b>Every 60s</b></span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")



# Load Data

df = load_data()


# Sidebar Controls
st.sidebar.header("🕹️ Pipeline Controls")
if st.sidebar.button("🔄 Stream New Event & Refresh", use_container_width=True):
    st.rerun()

st.sidebar.caption(f"**Data Pipeline:** {db_message}")
st.sidebar.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Filter Analytics")

state = st.sidebar.multiselect(
    "State",
    sorted(df["state"].dropna().unique())
)

city = st.sidebar.multiselect(
    "City",
    sorted(df["city"].dropna().unique())
)

blood_group = st.sidebar.multiselect(
    "Blood Group",
    sorted(df["blood_group"].dropna().unique())
)

event_type = st.sidebar.multiselect(
    "Event Type",
    sorted(df["event_type"].str.upper().dropna().unique())
)

# Apply Filters
filtered_df = df.copy()

if state:
    filtered_df = filtered_df[filtered_df["state"].isin(state)]

if city:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]

if blood_group:
    filtered_df = filtered_df[
        filtered_df["blood_group"].isin(blood_group)
    ]

if event_type:
    filtered_df = filtered_df[
        filtered_df["event_type"].str.upper().isin(event_type)
    ]

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter criteria. Try adjusting your filters.")
    st.stop()


# KPI Cards


total_events = len(filtered_df)

donations = (
    filtered_df["event_type"] == "DONATION"
).sum()

requests = (
    filtered_df["event_type"] == "REQUEST"
).sum()

transfers = (
    filtered_df["event_type"] == "TRANSFER"
).sum()

alerts = (
    filtered_df["event_type"] == "ALERT"
).sum()

available_units = (
    filtered_df["available_units"]
    .fillna(0)
    .sum()
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Total Events", total_events)
c2.metric("Donations", donations)
c3.metric("Requests", requests)
c4.metric("Transfers", transfers)
c5.metric("Alerts", alerts)
c6.metric("Available Units", int(available_units))

st.markdown("---")


# Blood Group Distribution

st.subheader(" Blood Group Distribution")

bg = (
    filtered_df["blood_group"]
    .value_counts()
    .reset_index()
)

bg.columns = ["Blood Group", "Count"]

fig = px.bar(
    bg,
    x="Blood Group",
    y="Count",
    color="Blood Group",
    text="Count"
)

fig.update_layout(
    height=450,
    xaxis_title="Blood Group",
    yaxis_title="Number of Events"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Blood Group Inventory


st.subheader(" Blood Group Inventory")

inventory_df = (
    filtered_df[
        filtered_df["event_type"] == "INVENTORY"
    ]
    .groupby("blood_group")["available_units"]
    .sum()
    .reset_index()
)

fig_inventory = px.bar(
    inventory_df,
    x="blood_group",
    y="available_units",
    color="blood_group",
    title="Available Units by Blood Group",
    text="available_units"
)

fig_inventory.update_layout(
    xaxis_title="Blood Group",
    yaxis_title="Available Units",
    showlegend=False
)

st.plotly_chart(fig_inventory, use_container_width=True)



# City-wise Events

st.subheader("City-wise Events")

city_df = (
    filtered_df["city"]
    .value_counts()
    .head(10)
    .reset_index()
)

city_df.columns = ["City", "Count"]

fig = px.bar(
    city_df,
    x="City",
    y="Count",
    color="Count",
    text="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")


# Hospital-wise Requests

st.subheader("🏥 Top Hospitals")

hospital_df = (
    filtered_df["hospital"]
    .value_counts()
    .head(10)
    .reset_index()
)

hospital_df.columns = ["Hospital", "Count"]

fig = px.bar(
    hospital_df,
    x="Hospital",
    y="Count",
    color="Count",
    text="Count"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Daily Event Trend

st.subheader("📈 Daily Event Trend")

trend_df = (
    filtered_df.groupby("event_date")
    .size()
    .reset_index(name="Events")
)

fig = px.line(
    trend_df,
    x="event_date",
    y="Events",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# Inventory by Blood Group

st.subheader("📦 Available Inventory")

inventory_df = (
    filtered_df.groupby("blood_group")["available_units"]
    .sum()
    .reset_index()
)

fig = px.bar(
    inventory_df,
    x="blood_group",
    y="available_units",
    color="blood_group",
    text="available_units"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# -----------------------------
# Latest Live Events
# -----------------------------
st.subheader("📋 Latest Live Events")

columns = [
    "event_id",
    "event_type",
    "blood_group",
    "blood_bank",
    "hospital",
    "city",
    "state",
    "units",
    "status",
    "processed_time"
]

st.dataframe(
    filtered_df[columns].head(50),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")



# Download CSV

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="blood_bank_data.csv",
    mime="text/csv"
)

st.markdown("---")



# Footer

st.markdown(
    """
    <hr>
    <center>
        <h4>Blood Bank Supply Chain Management Dashboard</h4>
        <p>Real-Time Data Engineering Project using Kafka • Spark Structured Streaming • AWS RDS • Streamlit</p>
    </center>
    """,
    unsafe_allow_html=True
)

