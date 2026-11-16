import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Room Monitoring",
    page_icon="🌡️",
    layout="wide"
)

# Load sensor dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sensor_data.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()

# Dashboard heading
st.title("🌡️ Smart Room Temperature & Humidity Monitoring")
st.caption("AWS Cloud-Based IoT Data Analytics Dashboard")

st.divider()

# KPI metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Readings", len(df))
col2.metric("Average Temperature", f"{df['Temperature'].mean():.2f} °C")
col3.metric("Average Humidity", f"{df['Humidity'].mean():.2f} %")
col4.metric("Maximum Temperature", f"{df['Temperature'].max():.2f} °C")

st.divider()

# Temperature monitoring
st.header("🌡️ Temperature Monitoring")

fig_temp = px.line(
    df,
    x="Timestamp",
    y="Temperature",
    color="Sensor_ID",
    title="Temperature Variation Over Time"
)

st.plotly_chart(fig_temp, use_container_width=True)

# Humidity monitoring
st.header("💧 Humidity Monitoring")

fig_humidity = px.line(
    df,
    x="Timestamp",
    y="Humidity",
    color="Sensor_ID",
    title="Humidity Variation Over Time"
)

st.plotly_chart(fig_humidity, use_container_width=True)

# Sensor-wise comparison
st.header("📊 Sensor-wise Comparison")

sensor_avg = (
    df.groupby("Sensor_ID")["Temperature"]
    .mean()
    .reset_index()
)

fig_sensor = px.bar(
    sensor_avg,
    x="Sensor_ID",
    y="Temperature",
    title="Average Temperature by Sensor"
)

st.plotly_chart(fig_sensor, use_container_width=True)

# Smart alerts
st.header("🚨 Smart Alerts")

alerts = df[
    (df["Temperature"] > 35) |
    (df["Humidity"] > 80)
]

st.warning(f"{len(alerts)} abnormal readings detected!")

st.dataframe(alerts, use_container_width=True)

# Complete dataset
st.header("📋 Complete Sensor Data")

st.dataframe(df, use_container_width=True)

st.success("Dashboard loaded successfully!")