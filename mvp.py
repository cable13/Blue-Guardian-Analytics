import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Page Configuration ---
st.set_page_config(page_title="HAB Forecaster MVP", page_icon="🌊", layout="wide")

# --- Header ---
st.title(" Spatiotemporal HAB Forecaster (MVP)")
st.markdown("**Status:** `Beta Prototyping` | **Backend:** `Synthetic Data (Pending NASA/NOAA API Integration)`")
st.markdown("---")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Model Parameters")
region = st.sidebar.selectbox(
    "Select Aquaculture Target Zone:",
    ["Chesapeake Bay (Sector 4)", "Gulf of Mexico (FL)", "Puget Sound (WA)"]
)

# Set base coordinates based on region selection
if "Chesapeake" in region:
    base_lat, base_lon = 38.5, -76.3
elif "Gulf" in region:
    base_lat, base_lon = 27.5, -83.5
else:
    base_lat, base_lon = 47.6, -122.4

forecast_days = st.sidebar.slider("Forecast Horizon (Days):", min_value=1, max_value=14, value=7)
run_model = st.sidebar.button("🚀 Run Spatial/Temporal Model")

# --- Main Dashboard ---
if run_model:
    with st.spinner('Querying synthetic satellite data & running prediction model...'):
        time.sleep(1.5) # Fake loading time to look like it's processing

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sea Surface Temp (SST)", "24.2 °C", "+1.2 °C Anomaly", delta_color="inverse")
col2.metric("Chlorophyll-a Conc.", "15.4 mg/m³", "+2.1 High", delta_color="inverse")
col3.metric("Wind Stress (Mixing)", "Low", "-5 knots")
col4.metric("Bloom Risk Probability", "87%", "+12% over 24hrs", delta_color="inverse")

st.markdown("---")

# Map and Chart Row
col_map, col_chart = st.columns([1.5, 1])

with col_map:
    st.subheader(f"📍 Predicted Bloom Trajectory: {region}")
    st.markdown("Displays simulated particle drift based on synthetic oceanographic currents.")
    
    # Generate fake geospatial data points around the selected region to simulate a bloom
    np.random.seed(42 if not run_model else None) # Randomize if button is clicked
    bloom_spread = np.random.randn(500, 2) / [60, 60]
    map_data = pd.DataFrame(
        bloom_spread + [base_lat, base_lon],
        columns=['lat', 'lon']
    )
    # Streamlit's built in map
    st.map(map_data, zoom=7, use_container_width=True)

with col_chart:
    st.subheader("📈 Risk Probability Timeline")
    st.markdown(f"Forecasting risk levels for the next **{forecast_days} days**.")
    
    # Generate fake time-series data for the chart
    dates = pd.date_range(start=pd.Timestamp.today(), periods=forecast_days)
    base_risk = 60
    # Create an upward trending risk curve
    risks = base_risk + np.cumsum(np.random.randint(-5, 15, size=forecast_days))
    risks = np.clip(risks, 0, 100) # Keep between 0 and 100%
    
    chart_data = pd.DataFrame({
        "Date": dates,
        "Probability of HAB (%)": risks
    }).set_index("Date")
    
    st.line_chart(chart_data, use_container_width=True)

# --- Automated Alert Section ---
st.markdown("---")
st.subheader("⚠️ Automated Action Plan")
if risks[-1] > 80:
    st.error(f"**CRITICAL ALERT:** Model predicts a {risks[-1]}% probability of an active harmful algal bloom intersecting the target zone by Day {forecast_days}. Recommend immediate preventative harvesting.")
else:
    st.success(f"**ALL CLEAR:** Risk levels remain manageable ({risks[-1]}%) over the forecast horizon. Continue normal aquaculture operations.")
