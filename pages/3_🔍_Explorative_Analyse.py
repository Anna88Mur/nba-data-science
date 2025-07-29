import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import numpy as np
from scipy.cluster.hierarchy import linkage, leaves_list


set_app_config(
    title="Explorative Analyse",
    icon="🔍",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Explorative Analyse</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="team-section">
    <h2>Inhalt</h2>
        <p></p>
        <ul>
            <li>Heatmaps zu Korrelationen physischer/spielerischer Merkmale mit Karriere-Erfolg</li>
            <li>Draft-Analysen</li>
            <li>Dreipunktewurf-Analysen</li>
        </ul>

</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(
    ["📈 Korrelationen", "📊 Draft-Analysen", "🔍 Dreipunktewurf-Analysen"])

with tab1:
    st.header("📈 Korrelationen")
    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    Heatmap mit Metriken: Korrelationen zwischen Combine-Daten und Karriereerfolg
    </div>
    """, unsafe_allow_html=True)

    # Daten laden
    numerical_data = pd.read_csv("data/numerical_data.csv")

    # Spalten entfernen
    drop_cols = ['stl_pct_calc', 'allstar_pct_calc', 'avg_age', 'stand_jump',
                 'max_jump', 'court_sprint', 'end_age', 'lane_agility',
                 'bench_press', 'fg_pct_calc', 'usg_pct_calc', 'orb_pct_calc',
                 'drb_pct_calc', 'net_rating_calc', 'all_star_total',
                 'score_guard', 'score_wing', 'score_big', 'score_nach_cluster',
                 'success_score']

    corr_data = numerical_data.drop(columns=drop_cols).corr()


# Variante 3

    def cluster_corr_matrix(corr_matrix):
        """Korrelationsmatrix nach Clustern sortieren"""
        # Berechnung der Distanzen zwischen den Merkmalen
        row_linkage = linkage(corr_matrix, method='ward', metric='euclidean')
        col_linkage = linkage(corr_matrix.T, method='ward', metric='euclidean')

        # Ermitteln der Reihenfolge der Zeilen und Spalten
        row_order = leaves_list(row_linkage)
        col_order = leaves_list(col_linkage)

        # Sortieren der Matrix
        clustered = corr_matrix.iloc[row_order, col_order]
        return clustered

    clustered_corr = cluster_corr_matrix(corr_data)
    clustered_corr = clustered_corr.iloc[::-1]

    # 2. Erstellung einer interaktiven, geclusterten Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=clustered_corr.values,
        x=clustered_corr.columns.tolist(),
        y=clustered_corr.index.tolist(),
        zmin=-1,
        zmax=1,
        colorscale='RdBu',
        colorbar=dict(title='Korrelation'),
        hoverongaps=False,
        text=np.round(clustered_corr.values, 2),
        texttemplate="%{text}",
    ))

    # 3. Layout-Anpassung
    fig.update_layout(
        title='Korrelationsmatrix mit hierarchischem Clustering',
        width=800,
        height=700,
        xaxis_title="Merkmale",
        yaxis_title="Merkmale",
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        margin=dict(l=100, r=50, b=150, t=50),
    )


    # 4. Hinzufügen von Annotationen zur besseren Lesbarkeit
    fig.update_traces(
        hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Korrelation: %{z:.2f}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    <strong>💡 Interpretation:</strong><br>
        Korrelationen zwischen:<br>
        <ul>
            <li>Karrierejahre, Spielminuten gesamt und Spielminuten pro Saison ➔ Indiz für Verfügbarkeit und Konstanz</li>
            <li>True Shooting, Box Plus Minus und Win Share</li>
            <li>Rebounds und Blocks ➔ positive Kor. zu Größe und Gewicht des Spielers ➔ Leistungsmetriken für große Defensivspieler</li>
            <li>Dreipunktewürfe und Assists  negative Kor. zu Größe und Gewicht des Spielers ➔ Leistungsmetriken für kleine Offensivspieler</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


with tab2:
    st.header("📊 Draft-Analysen")

    with st.expander("ℹ️ Kurze Information zum Draftverfahren"):
        st.markdown("""
        - **Jährliche Veranstaltung**, bei der Profiteams neue, junge Spieler auswählen dürfen  
        - **Ziel**: faire Talentverteilung, damit nicht immer nur die besten Teams die besten Talente bekommen  
        - **Schwächere Teams dürfen zuerst wählen**
        """)

    # Daten laden (Einrückung korrigiert!)
    draft = pd.read_csv("data/data_analyse_60_height_draft.csv")

    # Filter-Widgets
    st.subheader("🔍 Filter")
    col1, col2, col3, col4 = st.columns(4)

    with col2:
        d_group_filter = st.multiselect(
            "Draft-Gruppen (d_group):",
            options=sorted(draft['d_group'].unique()),
            default=draft['d_group'].unique()
        )

        st.markdown(
            "<i>Hinweis: Wenn du <b>7</b> auswählst, siehst du Spieler, die <b>nicht gedraftet</b> wurden.</i>",
            unsafe_allow_html=True)

    with col1:
        pos_filter = st.multiselect(
            "Positionsgruppe(n) (pos_cluster_calc):",
            options=sorted(draft['pos_cluster_calc'].unique()),
            default=sorted(draft['pos_cluster_calc'].unique())
        )

    with col3:
        draft_number_filter = st.multiselect("Draft-Nummern (z. B. 1–60 regulär, 61 = undrafted):",
                                             options=sorted(
                                                 draft['draft_number'].unique()),
                                             default=sorted(draft['draft_number'].unique()))

        st.markdown(
            "<i>Hinweis: Wenn du <b>61</b> auswählst, siehst du Spieler, die <b>nicht gedraftet</b> wurden.</i>",
            unsafe_allow_html=True)

    with col4:
        min_sum, max_sum = int(draft['sum_mp'].min()), int(
            draft['sum_mp'].max())
        sum_mp_range = st.slider(
            "Spielzeitbereich (sum_mp):",
            min_value=min_sum,
            max_value=max_sum,
            value=(min_sum, max_sum),
            step=100
        )

    # Filter anwenden
    gefiltert = draft[
        (draft['d_group'].isin(d_group_filter)) &
        (draft['pos_cluster_calc'].isin(pos_filter)) &
        (draft['draft_number'].isin(draft_number_filter)) &
        (draft['sum_mp'].between(sum_mp_range[0], sum_mp_range[1]))
    ]

    # Top 10
    top10_up = gefiltert[['player', 'pos_cluster_calc', 'sum_mp', 'all_star_total',
                         'draft_number', 'success_score', 'avg_score_d_number',
                          'score_d_number_diff', 'career_years'
                          ]].sort_values(by='score_d_number_diff', ascending=False).head(10)

    # Underperformer (nur gedraftete Spieler)
    nur_gedraftet = gefiltert[gefiltert['draft_number'] != 61]

    top10_down = nur_gedraftet[[
        'player', 'pos_cluster_calc', 'sum_mp', 'all_star_total',
        'draft_number', 'success_score', 'avg_score_d_number',
        'score_d_number_diff', 'career_years'
    ]].sort_values(by='score_d_number_diff', ascending=True).head(10)

    st.subheader("🏅 Top 10 Überperformer (inkl. Undrafted)")

    st.dataframe(
        top10_up.style.format({
            'sum_mp': lambda x: f'{x:,.0f}'.replace(',', '.'),
            'avg_score_d_number': '{:.2f}',
            'score_d_number_diff': '{:.2f}'
        }),
        use_container_width=True)

    st.subheader("🚫 Top 10 Busts (nur gedraftete Spieler)")
    st.dataframe(top10_down.style.format({
        'sum_mp': lambda x: f'{x:,.0f}'.replace(',', '.'),
        'avg_score_d_number': '{:.2f}',
        'score_d_number_diff': '{:.2f}'
    }),
        use_container_width=True)
    

    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
    💎 <b>Größter Draft Steal der Geschichte: Nikola Jokic</b><br>
    Nikola Jokic wurde im Jahr 2014 mit wenig Aufmerksamkeit an 41. Stelle von den Denver Nuggets ausgewählt und entwickelte sich innerhalb kürzester Zeit zu einem der besten Spieler. Seit 2019 wurde er jährlich ins All-Star-Team gewählt und erhielt in den Jahren 2021, 2022 und 2024 den großen Titel des Most Valuable Players.<br><br>
    
    💣 <b>Größter Draft Bust der Geschichte: Anthony Bennett</b><br>
    Anthony Bennett wurde im Jahr 2013 für Viele recht überraschend an erster Stelle von den Cavaliers ausgewählt. Er konnte den Erwartungen und dem Druck jedoch nicht standhalten. Seine erste Saison als Rookie war ein Desaster. Trotz mehrerer Versuche, seine Karriere bei verschiedenen Teams wiederzubeleben, war Bennett nach vier Saisons nicht mehr in der NBA.
    </div>
    """, unsafe_allow_html=True)


with tab3:
    st.header("🔍 Dreipunktewurf-Analysen")


    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
    <b> Analysefrage </b>: Hat Stephen Curry mit seinem Erfolg das Spielverhalten bzgl. der Dreipunktewürfe in der NBA beeinflusst?
    </div>
    """, unsafe_allow_html=True)

    # Daten laden
    merged_with_all_star_60 = pd.read_csv("data/merged_with_all_star_60.csv")

    # Ligadurchschnitt FG3% pro Saison
    fg3_by_season = merged_with_all_star_60.groupby(
        "season")["fg3_pct"].mean().reset_index()

    # Beispielwerte für Vergleichslinie
    val_94 = fg3_by_season[fg3_by_season["season"]
                           == 1994]["fg3_pct"].values[0]
    val_98 = fg3_by_season[fg3_by_season["season"]
                           == 1998]["fg3_pct"].values[0]

    # Spieler-Dropdown
    player_list = sorted(
        merged_with_all_star_60["player"].dropna().unique().tolist())
    player_name = st.selectbox(
        "🔍 Spieler wählen",
        options=player_list,
        index=player_list.index("LeBron James")
    )

    # Gefilterte Daten für den Spieler
    player_fg3_df = merged_with_all_star_60[merged_with_all_star_60['player'] == player_name]

    zeige_vergleichslinie = st.checkbox(
        "📉 Vergleichslinie (1994–1998) anzeigen", value=False)

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(12, 6))

    # Ligadurchschnitt

    sns.lineplot(data=fg3_by_season, x='season', y='fg3_pct',
                 marker='o', label='Ligadurchschnitt FG3%', ax=ax)

    # Vergleichslinie
    if zeige_vergleichslinie:
        ax.plot([1994, 1998], [val_94, val_98], color='red', linewidth=2,
                linestyle='--', label='Hypothetische Entwicklung')

    # Spielerlinie
    sns.lineplot(data=player_fg3_df, x='season', y='fg3_pct',
                 marker='o', color='orange', label=f'{player_name} FG3%', ax=ax)

    # Plot anpassen
    ax.set_title("Vergleich: FG3%-Entwicklung – Liga vs. Spieler")
    ax.set_xlabel("Saisonjahr")
    ax.set_ylabel("FG3%")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    # Plot anzeigen
    st.pyplot(fig)

    st.markdown("""
        <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
        <b>Antwort: Nein</b><br><br>

        <b>Wissenswertes:</b><br>
        • 1979/80: Einführung der Dreipunktelinie in der NBA<br>
        • Entfernung: 7,24 m vom Korb<br>
        • 1994–1997: Temporäre Verkürzung der Entfernung auf 6,75 m
        </div>
        """, unsafe_allow_html=True)
