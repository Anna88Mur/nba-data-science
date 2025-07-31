import streamlit as st
from style_utils import set_app_config, load_custom_css
from streamlit_mermaid import st_mermaid
from pathlib import Path
import base64

set_app_config(
    title="Unser Team",
    icon="👥",
    layout="wide"
)

load_custom_css()

st.markdown('<div class="centered-title">Unser Team</div>',
            unsafe_allow_html=True)



# Funktion: Lokales Bild in Base64 konvertieren
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Icons laden und konvertieren
linkedin_icon = img_to_base64("images/linkedin.png")
github_icon = img_to_base64("images/github.png")

# --- Team Abschnitt ---
st.markdown("""
<div class="team-section">
    <h2>Teammitglieder</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("images/Isabelle.png", width=200)
with col2:
    st.markdown(f"""
    <strong>Isabelle Haehl</strong>
    <a href="https://www.linkedin.com/in/isabelle-haehl" target="_blank">
        <img src="data:image/png;base64,{linkedin_icon}" width="20" style="margin-left:6px;">
    </a>
    <a href="https://github.com/isabellehaehl" target="_blank">
        <img src="data:image/png;base64,{github_icon}" width="20" style="margin-left:6px;">
    </a><br>
    Data Scientist
    <p> </p>
    🟠 Organisation der Aufgaben über Jira  <br>
    🟠 Deskriptive Analysen <br> 
    🟠 Definieren und Erstellen des Success Scores für die Analysen und ML-Modelle
    """, unsafe_allow_html=True)

col3, col4 = st.columns([1, 5])
with col3:
    st.image("images/Florian.jpg", width=200)
with col4:
    st.markdown(f"""
    <strong>Florian Löb</strong>
    <a href="https://www.linkedin.com/in/florian-loeb" target="_blank">
        <img src="data:image/png;base64,{linkedin_icon}" width="20" style="margin-left:6px;">
    </a>
    <a href="https://github.com/florian-loeb" target="_blank">
        <img src="data:image/png;base64,{github_icon}" width="20" style="margin-left:6px;">
    </a><br>
    Data Scientist  
    <p> </p>
    🟠 Projektstrukturierung und Koordination  <br>
    🟠 Entwicklung und Anwendung der ML-Modelle
    """, unsafe_allow_html=True)

col5, col6 = st.columns([1, 5])
with col5:
    st.image("images/Anna.jpeg", width=200)
with col6:
    st.markdown(f"""
    <strong>Anna Muravyeva</strong>
    <a href="https://www.linkedin.com/in/anna-muravyeva-3602b2374" target="_blank">
        <img src="data:image/png;base64,{linkedin_icon}" width="20" style="margin-left:6px;">
    </a>
    <a href="https://github.com/Anna88Mur" target="_blank">
        <img src="data:image/png;base64,{github_icon}" width="20" style="margin-left:6px;">
    </a><br>
    Data Analyst  
    <p> </p>
    🟠 Datenbeschaffung, -analyse und -aufbereitung  <br>
    🟠 Visualisierung und Darstellung der Projektergebnisse
    """, unsafe_allow_html=True)


st.markdown("""
<div class="team-section">
    <h2>Projektmotivation</h2>
    <p> </p>
        Dieses Projekt entstand aus der Leidenschaft für Datenanalyse und dem Wunsch, das Karrierepotenzial von NBA-Spielern besser verstehen zu können.
        Mit Hilfe von Machine Learning und explorativen Methoden analysieren wir die wichtigsten Einflussfaktoren auf den sportlichen Erfolg.
</div>
""", unsafe_allow_html=True)

fishbone = """

graph LR
    A[Warum dieses Projekt?] --> B1[Datenlücken]
    A --> B2[Subjektive Bewertungen]
    A --> B3[Scouting-Ineffizienz]
    
    B1 --> C1[Kein einheitlicher Erfolgsindex]
    B1 --> C2[Fragmentierte Stats]
    
    B2 --> C3[MVP-Debatten]
    B2 --> C4[Draft-Fehlentscheidungen]
    
    B3 --> C5[Übersehene Talente]
    B3 --> C6[Hohe finanzielle Risiken]

    """

st.divider()
st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

st.subheader("Warum haben wir uns für dieses Projekt entschieden??")

st_mermaid(fishbone, height=500)


st.markdown("""
<style>
.team-section ul {
    list-style-type: disc !important;
    margin-left: 20px;
    padding-left: 20px;
}
</style>

<div class="team-section">   
    <h2>Danksagung & Datenquellen</h2>
    <p> </p>
        Ein besonderer Dank gilt den Open-Data-Plattformen und der Basketball-Community, 
        die uns Zugang zu wertvollen Datensätzen ermöglicht haben:
    <ul>
        <li>basketball-reference.com</li>
        <li>NBA Stats API</li>
        <li>Kaggle</li>
    </ul>
</div>
""", unsafe_allow_html=True)
