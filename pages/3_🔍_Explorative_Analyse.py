import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

set_app_config(
    title="Explorative Analyse",
    icon="🔍",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Explorative Analyse</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Inhalt</h2>
        <p></p>
        <ul>
            <li>Heatmaps zu Korrelationen physischer/spielerischer Merkmale mit Karriere-Erfolg</li>
            <li>Boxplots z. B. Draftposition vs. PPG/All-Star-Status</li>
            <li>Streudiagramme (z. B. Minuten vs. Erfolg)</li>
        </ul>

</div>
""", unsafe_allow_html=True)