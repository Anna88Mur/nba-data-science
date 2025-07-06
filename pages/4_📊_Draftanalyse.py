import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

set_app_config(
    title="Draftanalyse",
    icon="📊",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Draftanalyse: Steals & Busts</div>',
            unsafe_allow_html=True)


st.markdown("""
<div class="team-section">
    <ul>
        <li><strong>Analyse: Erwartung vs. Realität (z. B. Draft-Rang vs. tatsächlicher Erfolg)</li>
        <li><strong>Gruppenvergleich (Top 10, Mid, Late Picks)</li>
        <li><strong>Liste besonders über- oder unterperformender Spieler</li>
    </ul>
</div>
""", unsafe_allow_html=True)            

