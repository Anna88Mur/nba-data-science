import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

set_app_config(
    title="MVP vs. Nicht-MVPs",
    icon="👑",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Hidden MVPs</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Inhalt</h2>
        <p></p>
        <ul>
            <li>Spieler mit MVP-würdigen Stats ohne Auszeichnung</li>
            <li>Filter nach Saison, Team, Stat</li>
            <li>Begründbare Vorschläge für verpasste MVP-Titel</li>
        </ul>

</div>
""", unsafe_allow_html=True)