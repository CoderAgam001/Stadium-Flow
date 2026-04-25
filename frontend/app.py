import streamlit as st
import requests
import pandas as pd
import os
from frontend.config import API_URL, APP_TITLE, CACHE_TTL, CROWD_ALERT_THRESHOLD, ADMIN_USERNAME, ADMIN_PASSWORD
from frontend.components import render_recommendation_card, render_live_counter

st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon="🏟️")

# Load external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("frontend/style.css")

# Suggestion 3: Unified Session State
if 'role' not in st.session_state:
    st.session_state.role = "guest"
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Header & Authentication Logic
col_title, col_login = st.columns([4, 1])
with col_title:
    st.title(f"🏟️ {APP_TITLE}")

with col_login:
    st.write("")
    if st.session_state.role == "admin":
        if st.button("Logout", key="logout_btn"):
            st.session_state.role = "guest"
            st.rerun()
    else:
        if st.button("Login as Admin", key="login_btn"):
            st.session_state.show_login = not st.session_state.show_login

# Login Form
if st.session_state.show_login and st.session_state.role != "admin":
    st.markdown("### Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            # Suggestion 7: Use credentials from config
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.session_state.show_login = False
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    # Stop rendering the rest of the app until logged in or cancelled
    st.stop() 

# Suggestion 2: Data Caching
@st.cache_data(ttl=CACHE_TTL)
def fetch_zones():
    try:
        response = requests.get(f"{API_URL}/zones")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend server is not reachable.")
    return []

def fetch_analytics():
    try:
        response = requests.get(f"{API_URL}/analytics")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

# ----------------- SHARED DATA -----------------
zones_data = fetch_zones()

# ----------------- ADMIN VIEW -----------------
if st.session_state.role == "admin":
    st.header("Admin Dashboard")
    
    col_dash_1, col_dash_2 = st.columns([4, 1.2])
    with col_dash_2:
        st.info("💡 Predictive Sync Active")
        if st.button("🔄 Manual Refresh"):
            st.cache_data.clear()
            st.rerun()

    if zones_data:
        df = pd.DataFrame(zones_data)
        df['Occupancy %'] = (df['current_occupancy'] / df['capacity']) * 100
        
        # Critical Alerts Only
        overcrowded = df[df['Occupancy %'] > CROWD_ALERT_THRESHOLD]
        if not overcrowded.empty:
            for _, row in overcrowded.iterrows():
                st.warning(f"🚨 **CRITICAL:** {row['zone_name']} is at {row['Occupancy %']:.1f}% capacity!")

        # Live Occupancy
        st.subheader("Live Occupancy")
        st.bar_chart(df.set_index('zone_name')['Occupancy %'], color="#e63946")
        
        with st.expander("View Raw Data"):
            df['Occupancy %'] = df['Occupancy %'].round(1)
            st.dataframe(
                df[['zone_id', 'zone_name', 'current_occupancy', 'capacity', 'Occupancy %']],
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("Connecting to sensor network...")

    # Sidebar Analytics exclusively for Admin
    with st.sidebar:
        st.header("📈 Prediction Log")
        analytics_data = fetch_analytics()
        if analytics_data:
            a_df = pd.DataFrame(analytics_data)
            st.dataframe(a_df, hide_index=True, height=400)
        else:
            st.info("Analytics stream offline.")

# ----------------- FAN VIEW (GUEST) -----------------
else:
    st.header("Find Your Way")
    
    if zones_data:
        zone_options = {z['zone_name']: z['zone_id'] for z in zones_data}
        
        col_start, col_dest = st.columns(2)
        with col_start:
            selected_start_name = st.selectbox("📍 Starting Point", list(zone_options.keys()), key="start_pos")
        with col_dest:
            selected_dest_name = st.selectbox("🏁 End Destination", list(zone_options.keys()), key="dest_pos")
        
        output_placeholder = st.empty()
        st.write("") 

        if st.button("🚀 Find Optimal Path", type="primary", use_container_width=True):
            start_id = zone_options[selected_start_name]
            dest_id = zone_options[selected_dest_name]
            
            if start_id == dest_id:
                st.info("You are already at your destination!")
            else:
                with st.spinner("Calculating optimal route..."):
                    try:
                        response = requests.get(f"{API_URL}/get_recommendation/{start_id}/{dest_id}")
                        if response.status_code == 200:
                            data = response.json()
                            with output_placeholder.container():
                                # Suggestion 1: Use Modular Component
                                render_recommendation_card(
                                    data.get('recommendation'),
                                    data.get('key_note'),
                                    data.get('distance')
                                )
                        else:
                            st.error(f"Routing Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")
    else:
        st.info("Waiting for stadium zone data...")

# ----------------- LIVE COUNTERS (BOTTOM) -----------------
if zones_data:
    washroom_occupancy = sum(z['current_occupancy'] for z in zones_data if "Washroom" in z['zone_name'])
    # Suggestion 1: Use Modular Component
    render_live_counter(washroom_occupancy)
