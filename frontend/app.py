import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Stadium Queue Rerouting", layout="wide", page_icon="🏟️")

# Black Theme CSS with Premium Aesthetics
st.markdown("""
    <style>
    /* Global background and font */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    /* Headers */
    h1, h2, h3 {
        color: #e63946 !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    /* Primary buttons */
    .stButton>button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff4d5a !important;
        box-shadow: 0 8px 25px rgba(230, 57, 70, 0.5) !important;
        transform: translateY(-2px);
    }
    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #111111;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #222222;
    }
    div[data-testid="stMetricValue"] {
        color: #e63946 !important;
        font-weight: 800;
    }
    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: #111111 !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #333333 !important;
    }
    /* Cards and containers */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px;
    }
    /* Explanation text */
    .feature-explanation {
        color: #888888;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #222222;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏟️ Stadium Flow: Smart Rerouting")
st.markdown("<p class='feature-explanation'>Optimizing stadium crowd flow using real-time predictive analytics and AI.</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Admin Dashboard", "🏃 Fan Navigation"])

def fetch_zones():
    try:
        response = requests.get(f"{API_URL}/zones")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend server is not reachable. Is FastAPI running on port 8000?")
    return []

with tab1:
    st.header("Admin: Real-time Occupancy")
    st.markdown("<p class='feature-explanation'>Monitor live crowd levels across stadium zones to identify potential bottlenecks.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1.2])
    with col2:
        st.info("💡 Keep data updated")
        if st.button("🔄 Sync Live Data", key="refresh_admin"):
            st.rerun()
        st.markdown("<p style='font-size: 0.8rem; color: #666;'>Pull the latest occupancy metrics from the stadium sensors.</p>", unsafe_allow_html=True)

    zones_data = fetch_zones()
    
    if zones_data:
        df = pd.DataFrame(zones_data)
        df['Occupancy %'] = (df['current_occupancy'] / df['capacity']) * 100
        
        st.subheader("Visual Flow Analytics")
        st.bar_chart(df.set_index('zone_name')['Occupancy %'], color="#e63946")
        
        st.subheader("Detailed Zone Metrics")
        st.dataframe(
            df[['zone_id', 'zone_name', 'current_occupancy', 'capacity', 'Occupancy %']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Connecting to sensor network... Please ensure backend is active.")

with tab2:
    st.header("Fan: Personalized Navigation")
    st.markdown("<p class='feature-explanation'>Navigate the stadium efficiently with AI-powered route recommendations to avoid busy queues.</p>", unsafe_allow_html=True)
    
    zones_data = fetch_zones()
    if zones_data:
        zone_options = {z['zone_name']: z['zone_id'] for z in zones_data}
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            selected_zone_name = st.selectbox("📍 Your Current Location", list(zone_options.keys()))
            st.markdown("<p class='feature-explanation'>Select your current location to receive tailored rerouting advice.</p>", unsafe_allow_html=True)
        
        with col_f2:
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("🚀 Find Optimal Path", type="primary"):
                user_zone_id = zone_options[selected_zone_name]
                
                with st.spinner("Analyzing crowd patterns..."):
                    try:
                        response = requests.get(f"{API_URL}/get_recommendation/{user_zone_id}")
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"**Recommendation:** {data.get('recommendation', 'No recommendation generated.')}")
                            st.markdown("<p class='feature-explanation'>AI suggested route based on the lowest predicted wait times.</p>", unsafe_allow_html=True)
                            
                            if "recommended_zone" in data:
                                st.metric(label="Estimated Walking Distance", value=f"{data['distance']} meters")
                        elif response.status_code == 404:
                            st.error("Zone not found.")
                        else:
                            st.error(f"Error: {response.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("Backend server is not reachable.")
    else:
        st.info("Waiting for stadium zone data...")
