import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

set_app_config(
    title="MVP vs. Nicht-MVPs",
    icon="🏀",
    layout="wide"
)
show_sidebar_info()
load_custom_css()



st.markdown('<div class="centered-title">MVP vs. Nicht-MVPs</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Inhalt</h2>
        <p></p>
        <ul>
            <li><a href="#boxplot-alter-der-mvp-kandidaten">📊 Boxplot: Alter der MVP-Kandidaten</a></li>
            <li><a href="#histogramm-altersverteilung-der-mvp-kandidaten">📈 Histogramm: Altersverteilung der MVP-Kandidaten</a></li>
            <li>Vergleich von Statistiken (PPG, WS, PER etc.)</li>
            <li>Histogramme, Boxplots</li>
            <li><a href="#durchschnittswerte-pro-saison">📅 Durchschnittswerte pro Saison</a></li>
        </ul>

</div>
""", unsafe_allow_html=True)


# --- CSV einlesen ---
df = pd.read_csv("NBA_Dataset.csv")

# --- MVP-Spieler herausfiltern ---
df_mvp = df[df['award_share'] > 0]


st.markdown("""
<div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    <strong>💡 Interpretation (was du im Vortrag sagen könntest):</strong><br>
    Die meisten Spieler, die MVP-Stimmen erhalten, sind zwischen <strong>25 und 30 Jahre alt</strong> – 
    also mitten in ihrer Prime. Nur wenige jüngere oder ältere Spieler schaffen es, Stimmen zu bekommen.
</div>
""", unsafe_allow_html=True)

# --- Boxplot: Alter der MVP-Spieler ---
# Anker: Boxplot
st.header("📊 Boxplot: Alter der MVP-Kandidaten")

fig1, ax1 = plt.subplots(figsize=(6,3))
sns.boxplot(data=df_mvp, x='age', color='skyblue', ax=ax1)
ax1.set_title('Alter der Spieler mit MVP-Stimmen (Boxplot)', fontsize=12)
ax1.set_xlabel('Alter')
ax1.grid(True)
st.pyplot(fig1)

# --- Histogramm: Alter der MVP-Spieler ---
st.header("📈 Histogramm: Altersverteilung der MVP-Kandidaten")

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.histplot(df_mvp['age'], bins=15, kde=True, color='purple', ax=ax2)
ax2.set_title('Verteilung des Alters der Spieler mit MVP-Stimmen', fontsize=12)
ax2.set_xlabel('Alter')
ax2.set_ylabel('Anzahl der Spieler')
ax2.grid(True)
st.pyplot(fig2)



df["is_mvp"] = df["award_share"] > 0
available_seasons = sorted(df["season"].dropna().unique())

st.header("📅 Durchschnittswerte pro Saison")
selected_season = st.selectbox("Wähle eine Saison:", available_seasons)

# Daten für diese Saison
season_df = df[df["season"] == selected_season]

# Mittelwerte berechnen
metrics = ["pts_per_g", "ast_per_g", "trb_per_g", "per", "ws"]

avg_values = season_df.groupby("is_mvp")[metrics].mean().reset_index()
avg_values["MVP Status"] = avg_values["is_mvp"].map({True: "MVP-Kandidaten", False: "Andere Spieler"})


# Melt für Seaborn
# melt() macht aus einer Matrix eine Liste – superpraktisch für Visualisierung oder lange Tabellen.
melted = avg_values.melt(id_vars="MVP Status", value_vars=metrics, var_name="Stat", value_name="Wert")

# Plotten
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=melted, x="Stat", y="Wert", hue="MVP Status", ax=ax)
ax.set_title(f"Durchschnittswerte in der Saison {selected_season}")
st.pyplot(fig)

st.markdown(f"""
<div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    <strong>💡 Interpretation:</strong><br>
    In der Saison <strong>{selected_season}</strong> zeigen MVP-Kandidaten im Durchschnitt deutlich höhere Werte 
    bei <em>Points per Game</em>, <em>Win Shares</em> und <em>Player Efficiency Rating</em> – was ihre wichtige Rolle im Team widerspiegelt.
</div>
""", unsafe_allow_html=True)