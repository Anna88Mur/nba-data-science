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
            <li><a href="#verteilung-mvp-stimmen">🏆 Verteilung MVP-Stimmenanteil</a></li>
            <li><a href="#durchschnittswerte-pro-saison">📅 Durchschnittswerte pro Saison</a></li>
            <li><a href="#effizienzvergleich-mvps-vs-nicht-mvps">🎯Effizienzvergleich: MVPs vs. Nicht-MVPs</a></li>
        </ul>

</div>
""", unsafe_allow_html=True)


# --- CSV einlesen ---
df = pd.read_csv("data/NBA_Dataset.csv")

df = df.reset_index()

# --- MVP-Spieler herausfiltern ---
df_mvp = df[df['award_share'] > 0]




# --- Boxplot: Alter der MVP-Spieler ---
# Anker: Boxplot
st.header("📊 Boxplot: Alter der MVP-Kandidaten")

fig1, ax1 = plt.subplots(figsize=(6,3))
sns.boxplot(data=df_mvp, x='age', color='skyblue', ax=ax1)
ax1.set_title('Alter der Spieler mit MVP-Stimmen (Boxplot)', fontsize=12)
ax1.set_xlabel('Alter')
ax1.grid(True)
st.pyplot(fig1)

st.markdown("""
<div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    <strong>💡 Interpretation:</strong><br>
    Die meisten Spieler, die MVP-Stimmen erhalten, sind zwischen <strong>25 und 30 Jahre alt</strong> – 
    also mitten in ihrer Prime. Nur wenige jüngere oder ältere Spieler schaffen es, Stimmen zu bekommen.
</div>
""", unsafe_allow_html=True)

old_mvps = df_mvp[df_mvp['age'] > 37]
if not old_mvps.empty:
    st.markdown("""
    <div style='padding: 0.5rem; background-color: #1f2633; border-radius: 0.5rem; margin-top: 1rem;'>
        <strong>📌 Hinweis:</strong> Folgende Spieler waren älter als 37 Jahre und erhielten dennoch MVP-Stimmen:
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(old_mvps[['player', 'age', 'season', 'award_share']], use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Histogramm: Alter der MVP-Spieler ---
st.header("📈 Histogramm: Altersverteilung der MVP-Kandidaten")

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.histplot(df_mvp['age'], bins=15, kde=True, color='purple', ax=ax2)
ax2.set_title('Verteilung des Alters der Spieler mit MVP-Stimmen', fontsize=12)
ax2.set_xlabel('Alter')
ax2.set_ylabel('Anzahl der Spieler')
ax2.grid(True)
st.pyplot(fig2)


# 📉 Histogramm der award_share-Werte (Stimmenanteil)
st.header("🏆 Verteilung MVP-Stimmenanteil", anchor="verteilung-mvp-stimmen")

fig_award, ax_award = plt.subplots(figsize=(10, 5))
sns.histplot(df_mvp['award_share'], bins=30, kde=True, color='green', ax=ax_award)
ax_award.set_title('Verteilung der MVP-Stimmen (nur Spieler mit Stimmen)')
ax_award.set_xlabel('MVP-Stimmenanteil (award_share)')
ax_award.set_ylabel('Anzahl der Spieler')
ax_award.grid(True)
st.pyplot(fig_award)

with st.expander("ℹ️ Interpretation der Verteilung der MVP-Stimmenanteile"):
    st.markdown(f"""
    Die Analyse der Variable **award_share** – also des Anteils der MVP-Stimmen eines Spielers – liefert interessante Erkenntnisse:

    - 🟢 **Viele Spieler erhalten nur einen sehr geringen Stimmenanteil** (knapp über 0). Das zeigt, dass sie zwar im Voting erscheinen, aber keine realistische Chance auf den Titel haben.
    - 🟡 **Wenige Spieler erreichen hohe Werte** (nahe 1.0). Diese Spieler dominieren das Voting und sind meist die tatsächlichen MVPs ihrer Saison.
                
    Um MVP zu werden, braucht man:

    🔹Den höchsten award_share der Saison

    🔹Typischerweise: award_share ≥ 0.80

    🔹Es muss nicht 1.0 sein, aber je näher, desto klarer der Sieg.            
    
    ➕ **Fazit:** Das MVP-Voting ist breit gefächert, aber nur wenige Ausnahmespieler stechen heraus. Ein hoher **award_share** ist ein starker Indikator für die sportliche Dominanz in einer Saison.
    
""", unsafe_allow_html=True)




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

metric_labels = {
    "pts_per_g": "Punkte/Spiel",
    "ast_per_g": "Assists/Spiel",
    "trb_per_g": "Rebounds/Spiel",
    "per": "Effizienzrating (PER)",
    "ws": "Gewinnanteil (WS)"
    }

melted["Stat"] = melted["Stat"].map(metric_labels)

# Plotten
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(data=melted, x="Stat", y="Wert", hue="MVP Status", ax=ax)
ax.set_title(f"Durchschnittliche Leistungskennzahlen von MVP-Kandidaten und anderen Spielern ({selected_season})")

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}", 
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', 
        va='center', 
        xytext=(0, 5), 
        textcoords='offset points'
    )

plt.xticks(rotation=15)
ax.set_xlabel("Leistungsmetriken")
ax.set_ylabel("Durchschnittswert")


st.pyplot(fig)

st.markdown(f"""

    <b>💡 Interpretation:</b><br><br>
    In der Saison <b>{selected_season}</b> zeigen MVP-Kandidaten im Durchschnitt deutlich höhere Werte 
    bei folgenden Statistiken:<br><br>

    🔹<b>PTS per Game</b> – Punkte pro Spiel: Wie viele Punkte ein Spieler im Durchschnitt erzielt.<br>
    🔹<b>AST per Game</b> – Assists pro Spiel: Wie oft ein Spieler seinen Mitspielern beim Punkten hilft.<br>
    🔹<b>TRB per Game</b> – Rebounds pro Spiel: Zurückgeholte Bälle nach Fehlwürfen.<br>
    🔹<b>PER</b> – Player Efficiency Rating: Eine umfassende Bewertungszahl für Effizienz und Gesamtleistung.<br>
    🔹<b>WS</b> – Win Shares: Schätzung, wie viel ein Spieler zum Teamerfolg beigetragen hat.<br><br>
    Diese Zahlen zeigen, dass MVP-Kandidaten sowohl in der Offensive als auch in der Gesamtwirkung herausragen.
""", unsafe_allow_html=True)



# --- Nur nötige Spalten und keine NaNs ---
effizienz_df = df[['is_mvp', 'ts_pct', 'efg_pct']].dropna()

# --- Gruppieren nach MVP vs. Nicht-MVP und Mittelwerte berechnen ---
effizienz_means = effizienz_df.groupby('is_mvp')[['ts_pct', 'efg_pct']].mean().T
effizienz_means.columns = ['Nicht-MVPs', 'MVP-Kandidaten'] if False in effizienz_means.columns else ['MVP-Kandidaten']

# --- Visualisierung ---
st.header("🎯Effizienzvergleich: MVPs vs. Nicht-MVPs")

fig, ax = plt.subplots(figsize=(7, 4))
effizienz_means.plot(kind='bar', ax=ax, color=['#2a9d8f', '#f4a261'])
ax.set_title('Durchschnittliche Effizienzmetriken (TS% und eFG%)', fontsize=14)
ax.set_ylabel('Wert')
ax.set_xlabel('Effizienz-Metrik')
ax.grid(axis='y')
ax.legend(title='Spielertyp', loc='lower right')
st.pyplot(fig)

# --- Interpretation ---
st.markdown(f"""

<b>💡 Interpretation:</b><br><br>
MVP-Kandidaten zeigen im Durchschnitt höhere Werte bei beiden Effizienzmetriken:<br><br>
🔹 <b>True Shooting % (TS%)</b>: berücksichtigt auch Freiwürfe und 3-Punkte-Würfe.<br>
🔹 <b>Effective FG%</b>: gewichtet 3-Punkte-Würfe stärker.<br><br>
Dies deutet darauf hin, dass MVPs nicht nur mehr punkten – sie tun es auch effizienter.

""", unsafe_allow_html=True)


