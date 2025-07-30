# Importiere notwendige Bibliotheken und Module
import os
import streamlit as st
import pandas as pd
import plotly.express as px
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

📊 Auf dieser Startseite findest du zentrale KPIs, die zeigen, wie einzigartig und von Erfolgen geprägt die Geschichte der NBA ist.<br>
    <div style='text-align: right; font-size: 0.85rem; margin-top: 2rem;'>
            Unsere Datenanalyse wurde mit Stand Juli 2025 durchgeführt.
    </div>        
</div>
""", unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)


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


st.markdown("<br><br>", unsafe_allow_html=True)

col7, col8, col9 = st.columns(3)

col7.metric("🔥 Playoff-Rekordpunkte", "63 Punkte", "Michael Jordan 1986")
col7.image("images/jordan_playoff.jpg", caption="Jordan", width=120)

col8.metric("💎 Meiste MVPs", "Kareem Abdul-Jabbar", "6 MVPs")
col8.image("images/kareem_logo.jpg", caption="Lakers", width=120)

col9.metric("✊ Erster afroamerikanischer NBA-Spieler", "Earl Lloyd", "1950")
col9.image("images/earl_lloyd.jpg", caption="Washington Capitols", width=120)

st.markdown("<br><br><br>", unsafe_allow_html=True)

st.divider()

st.markdown("## 🕰️ Historische Meilensteine")
st.markdown("Ein Blick zurück auf wichtige Momente in der NBA-Geschichte.")

milestones = pd.DataFrame({
    "Spieler": [
        "Bill Russell", "Wilt Chamberlain", "Kareem Abdul-Jabbar",
        "Larry Bird", "Magic Johnson", "Michael Jordan", "Shaquille O'Neal",
        "Kobe Bryant", "Tim Duncan", "Dirk Nowitzki", "LeBron James", "Stephen Curry"
    ],
    "Ereignis": [
        "🏆 11× NBA Champion, 5× MVP, 12× All-Star",
        "💯 100 Punkte in einem Spiel (1962), 2× NBA Champion,13x All Star,4x MVP",
        "🏀 Meiste Karrierepunkte bis 2023, 6× MVP, 15x All-NBA",
        "🎯 3× MVP in Folge, 3× Champion mit Celtics",
        "⚡ Rookie-Finals-MVP, 5× Champion mit Lakers, 3x MVP",
        "🐐 6× Champion, 5× MVP, 10× Scoring Leader, 14x All Star",
        "🔒 3× Finals MVP, dominant in der Zone, 15x All Star",
        "🎯 81 Punkte in einem Spiel, 5× NBA Champion, 18x All Star",
        "🌟 2× MVP, 5× Champion mit Spurs, Mr. Fundament, 15x All Star",
        "🇩🇪 2007 MVP, 2011 Champion, bester Europäer",
        "👑 All-Time Top Scorer, 4× Champion, 4× MVP",
        "🎯 4× Champion, 2× MVP, Revolution des Dreiers"
    ],
    "Start": [
        "1956-11-01", "1959-10-24", "1969-10-18",
        "1979-10-12", "1979-10-12", "1984-10-26", "1992-11-06",
        "1996-11-03", "1997-10-31", "1998-02-05", "2003-10-29", "2009-10-28"
    ],
    "Ende": [
        "1969-05-05", "1973-04-01", "1989-06-28",
        "1992-04-30", "1996-05-02", "2003-04-16", "2011-04-13",
        "2016-04-13", "2016-05-12", "2019-04-10", "2025-07-01", "2025-07-01"
    ]
})


milestones["Start"] = pd.to_datetime(milestones["Start"])
milestones["Ende"] = pd.to_datetime(milestones["Ende"])

milestones["Start_Jahr"] = milestones["Start"].dt.year
milestones["Ende_Jahr"] = milestones["Ende"].dt.year

fig = px.timeline(
    milestones,
    x_start="Start",
    x_end="Ende",
    y="Spieler",
    color="Spieler",
    custom_data=["Ereignis", "Start_Jahr", "Ende_Jahr"],
    title="Historische Karrieren der NBA-Legenden"
)

fig.update_yaxes(autorange="reversed")  # wichtig für Timeline
fig.update_layout(
    template="plotly_dark",
    height=650,
    margin=dict(l=20, r=20, t=60, b=20),
    title_font_size=22,
    xaxis=dict(
        tickformat="%Y",    # Nur Jahr anzeigen
        tick0="1950-01-01",
        dtick="M60",        # alle 60 Monate = 5 Jahre
    )
)

fig.update_traces(
    hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>Karriere: %{customdata[1]} – %{customdata[2]}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📊 Entdecke weitere Analysen im Menü links!")
