import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Stadium Queue Rerouting", layout="wide", page_icon="🏟️")

# Load external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("frontend/style.css")

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
        st.info("💡 Predictive Sync Active")
        if st.button("🔄 Manual Refresh", key="refresh_admin"):
            st.rerun()
        st.markdown("<p style='font-size: 0.8rem; color: #666;'>Occupancy trends are updated every 10 seconds.</p>", unsafe_allow_html=True)

    zones_data = fetch_zones()
    
    if zones_data:
        df = pd.DataFrame(zones_data)
        df['Occupancy %'] = (df['current_occupancy'] / df['capacity']) * 100
        
        # Overcrowding Alerts
        overcrowded = df[df['Occupancy %'] > 90]
        if not overcrowded.empty:
            for _, row in overcrowded.iterrows():
                st.warning(f"🚨 **ALERT:** {row['zone_name']} is critically crowded ({row['Occupancy %']:.1f}%)!")

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
                
                with st.spinner("Analyzing crowd patterns and trends..."):
                    try:
                        response = requests.get(f"{API_URL}/get_recommendation/{user_zone_id}")
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"**AI Recommendation:** {data.get('recommendation', 'No recommendation generated.')}")
                            
                            if data.get('recommended_zone') and data['recommended_zone'] != "None":
                                st.metric(label=f"Destination: {data['recommended_zone']}", value=f"{data['distance']} meters")
                                st.markdown("<p class='feature-explanation'>AI analyzed current occupancy and trends to find this optimal path.</p>", unsafe_allow_html=True)
                        elif response.status_code == 404:
                            st.error("Zone not found.")
                        else:
                            st.error(f"Error: {response.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("Backend server is not reachable.")
    else:
        st.info("Waiting for stadium zone data...")

# Sidebar Analytics for trends
with st.sidebar:
    st.header("📈 Prediction Log")
    st.markdown("<p style='font-size: 0.8rem; color: #888;'>Real-time occupancy logs for AI trend analysis.</p>", unsafe_allow_html=True)
    try:
        analytics_resp = requests.get(f"{API_URL}/analytics")
        if analytics_resp.status_code == 200:
            analytics_data = analytics_resp.json()
            if analytics_data:
                a_df = pd.DataFrame(analytics_data)
                st.dataframe(a_df, hide_index=True, height=400)
    except:
        st.info("Analytics stream offline.")
