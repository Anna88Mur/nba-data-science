# Importiere notwendige Bibliotheken und Module
import os
import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

os.chdir(os.path.dirname(__file__))



set_app_config(
    title="NBA Data Science Projekt",
    icon="🏀",
    layout="wide"
)

show_sidebar_info()

load_custom_css()

st.markdown('<div class="centered-title">🏀 NBA Data Science Projekt</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("nba2.jpg", width=900)

# Zeige eine Information mit zusätzlichen Hinweisen zur Bedienung der App
st.markdown("""
<div class="team-section">
    <h2>👋 Willkommen zu unserem NBA-Projekt!</h2> 
Tauche ein in die faszinierende Welt des Basketballs und erlebe die spannende Geschichte der NBA durch die Linse der Datenanalyse.

Unsere Anwendung richtet sich sowohl an leidenschaftliche Basketballfans als auch an professionelle Sportanalysten.  
Wir haben spannende Auswertungen zusammengestellt, um die großen Momente und Muster des Spiels sichtbar zu machen.

📊 Auf dieser Startseite findest du zentrale KPIs, die zeigen, wie einzigartig und von Erfolgen geprägt die Geschichte der NBA ist.
</div>
""", unsafe_allow_html=True)


col4, col5, col6 = st.columns(3)

col4.metric("🏆 Erste Meistermannschaft", "Philadelphia Warriors", "1947")
col4.image("images/warriors_logo.png",
           caption="Warriors", width=120)

col5.metric("📈 Längste Siegesserie", "33 Spiele", "L.A. Lakers 1971/72")
col5.image("images/lakers_logo.png", caption="Lakers", width=150)

col6.metric("🔥 Punkterekord in einem Spiel", "100 Punkte",
            "Wilt Chamberlain (Philadelphia Warriors, 1962)")
col6.image("images/chamberlain.jpg",
           caption="Wilt Chamberlain", width=120)


st.markdown("### 🌟 Weitere Fakten")

col7, col8, col9 = st.columns(3)

col7.metric("🔥 Playoff-Rekordpunkte", "63 Punkte", "Michael Jordan 1986")
col7.image("images/jordan_playoff.jpg", caption="Jordan", width=120)

col8.metric("💎 Meiste MVPs", "Kareem Abdul-Jabbar", "6 MVPs")
col8.image("images/kareem_logo.jpg", caption="Lakers", width=120)

col9.metric("✊ Erster afroamerikanischer NBA-Spieler", "Earl Lloyd", "1950")
col9.image("images/earl_lloyd.jpg", caption="Washington Capitols", width=120)


st.markdown("### 📊 Entdecke weitere Analysen im Menü links!")
