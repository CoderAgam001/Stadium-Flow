import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Stadium Queue Rerouting", layout="wide", page_icon="🏟️")

# Premier League Theme CSS
st.markdown("""
    <style>
    /* Global background and font */
    .stApp {
        background-color: #f4f4f6;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    /* Headers */
    h1, h2, h3 {
        color: #e63946 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    /* Primary buttons */
    .stButton>button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 6px rgba(230, 57, 70, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #c1121f !important;
        box-shadow: 0 6px 12px rgba(230, 57, 70, 0.3) !important;
        transform: translateY(-2px);
    }
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #e63946 !important;
        font-weight: 700;
    }
    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    /* Cards and containers */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏟️ Predictive Queue Rerouting App")
st.markdown("### 🏏 Cricket Stadium Crowd Management")

tab1, tab2 = st.tabs(["Admin Dashboard", "Fan View"])

def fetch_zones():
    try:
        response = requests.get(f"{API_URL}/zones")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend server is not reachable. Is FastAPI running on port 8000?")
    return []

with tab1:
    st.header("Admin View: Real-time Occupancy")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Refresh Data", key="refresh_admin"):
            st.rerun()

    zones_data = fetch_zones()
    
    if zones_data:
        df = pd.DataFrame(zones_data)
        df['Occupancy %'] = (df['current_occupancy'] / df['capacity']) * 100
        
        st.bar_chart(df.set_index('zone_name')['Occupancy %'], color="#e63946")
        
        st.dataframe(
            df[['zone_id', 'zone_name', 'current_occupancy', 'capacity', 'Occupancy %']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No data available.")

with tab2:
    st.header("Fan View: Find Your Way")
    
    zones_data = fetch_zones()
    if zones_data:
        zone_options = {z['zone_name']: z['zone_id'] for z in zones_data}
        
        selected_zone_name = st.selectbox("My Current Location", list(zone_options.keys()))
        
        if st.button("Find Shortest Path", type="primary"):
            user_zone_id = zone_options[selected_zone_name]
            
            with st.spinner("Finding best route..."):
                try:
                    response = requests.get(f"{API_URL}/get_recommendation/{user_zone_id}")
                    if response.status_code == 200:
                        data = response.json()
                        st.success(data.get("recommendation", "No recommendation generated."))
                        
                        if "recommended_zone" in data:
                            st.metric(label="Distance to new zone", value=f"{data['distance']} meters")
                    elif response.status_code == 404:
                        st.error("Zone not found.")
                    else:
                        st.error(f"Error: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend server is not reachable.")
    else:
        st.info("No zone data available to select.")
