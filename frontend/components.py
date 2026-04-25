import streamlit as st

def render_recommendation_card(recommendation, key_note, distance):
    """
    Renders a premium AI route recommendation card with 20% reduced width effect.
    """
    col_pad1, col_content, col_pad2 = st.columns([0.1, 0.8, 0.1])
    with col_content:
        st.markdown(f"""
        <div style="background-color: #111111; padding: 20px; border-radius: 12px; border-left: 5px solid #e63946; margin: 10px 0;">
            <h4 style="color: #e63946; margin-bottom: 10px;">🗺️ AI Route Recommendation</h4>
            <p style="color: white; font-size: 1.1rem; margin-bottom: 15px;">{recommendation}</p>
            <hr style="border-top: 1px solid #333; margin: 10px 0;">
            <p style="color: #ffaa00; font-weight: bold; margin-bottom: 5px;">⚠️ Key Note:</p>
            <p style="color: #bbbbbb; font-size: 0.95rem; margin-bottom: 15px;">{key_note}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; background: #222; padding: 10px; border-radius: 8px;">
                <span style="color: #888;">Estimated Distance:</span>
                <span style="color: #e63946; font-size: 1.2rem; font-weight: bold;">{distance} meters</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_live_counter(washroom_occupancy):
    """
    Renders the live facility counter at the bottom of the page.
    """
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: #0e1117; padding: 20px; border-radius: 15px; border: 1px solid #222; text-align: center; margin-top: 20px;">
            <p style="color: #888; font-size: 1rem; margin-bottom: 5px;">Total Live Washroom Occupancy</p>
            <h2 style="color: #e63946; font-size: 2.5rem; margin: 0;">{washroom_occupancy}</h2>
            <p style="color: #444; font-size: 0.8rem; margin-top: 10px;">Monitoring all facility zones in real-time</p>
        </div>
    """, unsafe_allow_html=True)
