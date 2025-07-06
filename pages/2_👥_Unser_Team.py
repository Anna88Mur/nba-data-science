import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css

set_app_config(
    title="Unser Team",
    icon="👥",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Unser Team</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Teammitglieder</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("images/Isabelle.png", width=200)

with col2:
    st.markdown("""
    **Isabelle Haehl**  
    Data Analyst  
    [LinkedIn](https://www.linkedin.com/in/alexmustermann) | [GitHub](https://github.com/alexmustermann)
    
    <br>
    🟠 Organisation der Aufgaben über Jira  
    🟠 Deskriptive Analysen  
    🟠 Machine Learning
    """, unsafe_allow_html=True)          

col3, col4 = st.columns([1, 5])
with col3:
    st.image("images/Florian.jpg", width=200)

with col4:
    st.markdown("""
    **Florian Löb**  
    Data Analyst  
    [LinkedIn](https://www.linkedin.com/in/alexmustermann) | [GitHub](https://github.com/alexmustermann)
    <br>
    🟠 Projektstrukturierung und Koordination  
    🟠 Entwicklung und Anwendung von Machine Learning Modellen
    """, unsafe_allow_html=True)

col5, col6 = st.columns([1, 5])
with col5:
    st.image("images/Anna.jpg", width=200)

with col6:
    st.markdown("""
    **Anna Muravyeva**  
    Data Analyst  
    [LinkedIn](https://www.linkedin.com/in/alexmustermann) | [GitHub](https://github.com/alexmustermann)
    <br>
    🟠 Datenbeschaffung, -analyse und -aufbereitung  
    🟠 Visualisierung und Darstellung der Projektergebnisse
    """, unsafe_allow_html=True)    


st.markdown("""
<div class="team-section">
    <h2>Projektmotivation</h2>
    <p>
        Dieses Projekt entstand aus der Leidenschaft für Datenanalyse und dem Wunsch, das Karrierepotenzial von NBA-Spielern besser verstehen zu können.
        Mit Hilfe von Machine Learning und explorativen Methoden analysieren wir die wichtigsten Einflussfaktoren auf den sportlichen Erfolg.
    </p>
</div>
""", unsafe_allow_html=True)
    
st.markdown("""
<div class="team-section">   
            <h2>Danksagung & Datenquellen</h2>
    <p>
        Ein besonderer Dank gilt den Open-Data-Plattformen und der Basketball-Community, die uns Zugang zu wertvollen Datensätzen ermöglicht haben:
    </p>
    <ul>
        <li>basketball-reference.com</li>
        <li>NBA Stats API</li>
        <li>Kaggle NBA Datasets</li>
    </ul>
</div>
""", unsafe_allow_html=True)

