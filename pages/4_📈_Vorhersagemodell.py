import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

set_app_config(
    title="MachineLearning",
    icon="📈",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">📈Vorhersagemodell (ML)</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Inhalt</h2>
        <p></p>
        <ul>
            <li>Modellinput: Draftdaten, Combine-Stats, Teamkontext</li>
            <li>Ausgabe: Prognose des „success_score“</li>
            <li>Visualisierung: Feature-Importances</li>
            <li>Möglichkeit, neuen Spieler einzugeben und Prognose zu erhalten</li>
        </ul>

</div>
""", unsafe_allow_html=True)