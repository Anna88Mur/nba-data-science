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

📊 Auf dieser Startseite findest du zentrale KPIs, die zeigen, wie einzigartig und von Erfolgen geprägt die Geschichte der NBA ist.
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
        "Kareem Abdul-Jabbar", "Larry Bird", "Michael Jordan",
        "Kobe Bryant", "LeBron James", "Stephen Curry",
        "Bill Walton", "Magic Johnson", "Julius Erving",
        "Shaquille O'Neal", "Dirk Nowitzki"
    ],
    "Ereignis": [
        "11 Meisterschaften, 12 Mal NBA ALL-STAR, 5 Mal MVP",  # 50er–60er
        "100 Punkte in einem Spiel Am 2. März 1962 erzielte er in einem Spiel gegen die New York Knicks ganze 100 Punkte,ein in der NBA bis heute unerreichter Rekord",                  # 1962
        "Meiste Karrierepunkte (1984 Rekord), 50 Greatest Players in NBA History",        # Einstieg
        "1. MVP mit Milwaukee (1971), Bester Korbschütze der NBA",                # 1971
        "3 MVPs in Folge",                            # 1984–86
        "Er wurde fünfmal als Wertvollster Spieler der NBA ausgezeichnet",                          # 1991–98
        "81 Punkte Spiel",                            # 2006
        "Basketball hero LeBron James is the NBA's all-time top scorer",                            # 2023
        "4x Meister,  NBA three-point scoring leader",                                 # ab 2015
        "Finals MVP mit Blazers",                     # 1977
        "Finals MVP als Rookie",                      # 1980
        "ABA-Legende & NBA-MVP",                      # 1976–81
        "3x Finals MVP",                              # 2000–2002
        "Erster Europäer mit MVP",                    # 2007
    ],
    "Start": [
        "1957-01-01", "1962-03-02", "1984-10-26",
        "1971-05-01", "1984-01-01", "1991-01-01",
        "2006-01-22", "2023-02-07", "2015-06-16",
        "1977-06-05", "1980-05-16", "1976-01-01",
        "2000-06-01", "2007-05-06"
    ]
})


milestones["Start"] = pd.to_datetime(milestones["Start"])
milestones["Ende"] = milestones["Start"] + pd.DateOffset(days=90)  # längere Balken

fig = px.timeline(
    milestones,
    x_start="Start",
    x_end="Ende",
    y="Spieler",
    color="Spieler",
    custom_data=["Ereignis"],
    title="Historische Meilensteine – NBA"
)

fig.update_yaxes(autorange="reversed")  # wichtig für Timeline
fig.update_layout(
    template="plotly_dark",
    height=600,
    margin=dict(l=20, r=20, t=60, b=20),
    title_font_size=22
)
fig.update_traces(
    hovertemplate="<b>%{y}</b><br>%{customdata[0]}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📊 Entdecke weitere Analysen im Menü links!")
