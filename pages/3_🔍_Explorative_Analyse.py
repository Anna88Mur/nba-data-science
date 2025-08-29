import streamlit as st
from style_utils import set_app_config, load_custom_css, apply_dark_theme
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

load_custom_css()

st.markdown('<div class="centered-title">Explorative Analyse</div>',
            unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(
    ["📈 Korrelationen", "📊 Draft-Analysen", "🔍 Dreipunktewurf-Analysen"])

with tab1:
    # st.header("📈 Korrelationen")
    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633 ; border-radius: 0.5rem;'>
    Heatmap mit Metriken: Korrelationen zwischen Combine-Daten und Leistungsmetriken
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
            <li>Dreipunktewürfe und Assists ➔ negative Kor. zu Größe und Gewicht des Spielers ➔ Leistungsmetriken für kleine Offensivspieler</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


with tab2:
    # st.header("📊 Draft-Analysen")

    with st.expander("ℹ️ Kurze Information zum Draftverfahren"):
        st.markdown("""
        - **Jährliche Veranstaltung**, bei der Profiteams neue, junge Spieler auswählen dürfen  
        - **Ziel**: faire Talentverteilung, damit nicht immer nur die besten Teams die besten Talente bekommen  
        - **Schwächere Teams dürfen zuerst wählen**
        """)

    # Daten laden
    draft = pd.read_csv("data/data_analyse_60_height_draft.csv")

    # Plot erzeugen
    apply_dark_theme()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=draft, x='d_group',
                y='success_score',
                palette='Set2',
                boxprops=dict(edgecolor='white', linewidth=1.5),
                whiskerprops=dict(color='white', linewidth=1.5),
                capprops=dict(color='white', linewidth=1.5),
                flierprops=dict(marker='o', markersize=4,
                                markerfacecolor='none', markeredgecolor='white'),
                medianprops=dict(color='white', linewidth=2),
                ax=ax)
    ax.set_title('Karriere-Erfolg nach Draftgruppe')
    ax.set_xlabel('Draftgruppe')
    ax.set_ylabel('Success Score')
    ax.grid(True, axis='y')

    plt.tight_layout()

    # 👉 In Streamlit anzeigen
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.pyplot(fig)

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
            "<i>Hinweis: Wenn du <b>7</b> auswählst, siehst du Spieler, die <b>nicht gedraftet</b> wurden.<br>"
            "Jede Gruppe besteht aus <b>10 Draftnummern</b> (z. B. Gruppe 1 = 1–10, Gruppe 2 = 11–20, …)"
            "</i>",
            unsafe_allow_html=True)

    with col1:
        pos_filter = st.multiselect(
            "Positionsgruppen (pos_cluster_calc):",
            options=sorted(draft['pos_cluster_calc'].unique()),
            default=sorted(draft['pos_cluster_calc'].unique())
        )

    with col3:
        draft_number_filter = st.multiselect("Draft-Nummern (draft_number):",
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
            'success_score': '{:.1f}',
            'avg_score_d_number': '{:.1f}',
            'score_d_number_diff': '{:.1f}'
        }),
        use_container_width=True
    )

    st.subheader("🚫 Top 10 Busts (nur gedraftete Spieler)")
    st.dataframe(
        top10_down.style.format({
            'sum_mp': lambda x: f'{x:,.0f}'.replace(',', '.'),
            'success_score': '{:.1f}',
            'avg_score_d_number': '{:.1f}',
            'score_d_number_diff': '{:.1f}'
        }),
        use_container_width=True
    )

    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
    💎 <b>Größter Draft Steal der Geschichte: Nikola Jokic</b><br>
    Nikola Jokic wurde im Jahr 2014 mit wenig Aufmerksamkeit an 41. Stelle von den Denver Nuggets ausgewählt und entwickelte sich innerhalb kürzester Zeit zu einem der besten Spieler. Seit 2019 wurde er jährlich ins All-Star-Team gewählt und erhielt in den Jahren 2021, 2022 und 2024 den großen Titel des Most Valuable Players.<br><br>
    
    💣 <b>Größter Draft Bust der Geschichte: Anthony Bennett</b><br>
    Anthony Bennett wurde im Jahr 2013 für Viele recht überraschend an erster Stelle von den Cavaliers ausgewählt. Er konnte den Erwartungen und dem Druck jedoch nicht standhalten. Seine erste Saison als Rookie war ein Desaster. Trotz mehrerer Versuche, seine Karriere bei verschiedenen Teams wiederzubeleben, war Bennett nach vier Saisons nicht mehr in der NBA.<br><br>
    🚀 <b>Bester nicht gedrafteter Spieler der Geschichte: Ben Wallace</b><br>
    Ben Wallace wurde 1996 im NBA-Draft nicht ausgewählt. Dennoch hatte er eine lange und erfolgreiche 16-jährige Karriere und wurde viermal ins NBA-All-Star-Team berufen.<br>
             
    </div>
    """, unsafe_allow_html=True)


with tab3:
    # st.header("🔍 Dreipunktewurf-Analysen")

    st.markdown("""
    <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
    <b> Analysefrage </b>: Wie hat sich der Spielstil historisch im Hinblick auf Dreipunktwürfe verändert? – Analyse auf Liga- und Spielerebene
    <br><br>
        <b>Hinweise zur Interpretation:</b><br><br>
        - Werte über 100 (bei Normalisierung) bedeuten eine Verbesserung gegenüber dem Basisjahr.<br>
        - Die Liga-Durchschnittswerte sind als Linien dargestellt, Spielerwerte als zusätzliche farbige Linien.<br>
        - Aktivieren Sie die Checkboxen, um den Anteil der Dreierwürfe und die Normalisierung einzublenden.<br>
        <b>- FG3% - Dreipunkt-Wurfquote</b> → Zeigt, wie sich die Trefferquote bei Dreipunktwürfen verbessert hat.<br>
        <b>- FG3A/FGA% - Anteil der Dreipunktwurfversuche an allen Wurfversuchen</b> → Zeigt, wie stark der Anteil der Dreierwürfe am gesamten Wurfvolumen gestiegen ist.
    </div>
    """, unsafe_allow_html=True)

    # Daten laden
    # merged_with_all_star_60 = pd.read_csv("data/merged_with_all_star_60.csv")
    NBA_3_Punkte = pd.read_csv("data/NBA_Dataset.csv")

    basisjahr=1982
    #  --- Ligadurchschnitt ---
    # - fg3_pct- - Zeigt, wie sich die Trefferquote bei Dreipunktwürfen verbessert hat
    # - fg3a_per_fga_pct - - Zeigt, wie stark der Anteil der Dreierwürfe am gesamten Wurfvolumen gestiegen ist.

    fg3_by_season = NBA_3_Punkte.groupby("season")["fg3_pct"].mean().reset_index()
    fg3a_share_by_season = NBA_3_Punkte.groupby("season")["fg3a_per_fga_pct"].mean().reset_index()



    # Spieler-Dropdown
    player_list = [""] + sorted(
        NBA_3_Punkte["player"].dropna().unique().tolist())
    player_name = st.selectbox(
        "🔍 Spieler wählen",
        options=player_list,
        index=0
    )
    # Checkboxen
    zeige_fg3a = st.checkbox("📈 Anteil der Dreierwürfe anzeigen (FG3A/FGA%)", value=False)
    normalisiert = st.checkbox("📊 Normalisierung (Basisjahr 1982 = 100)", value=False)

    # Gefilterte Daten für den Spieler (wenn vorhanden)
    if player_name:
        player_df = NBA_3_Punkte[NBA_3_Punkte['player'] == player_name]
        player_fg3_by_season = player_df.groupby("season")["fg3_pct"].mean().reset_index()
        player_fg3a_by_season = player_df.groupby("season")["fg3a_per_fga_pct"].mean().reset_index()


    # Normalisierung, falls aktiviert
    if normalisiert:
        fg3_norm = fg3_by_season.copy()
        fg3a_norm = fg3a_share_by_season.copy()
        
        fg3_basiswert = fg3_norm[fg3_norm["season"] == basisjahr]["fg3_pct"].values[0]
        fg3a_basiswert = fg3a_norm[fg3a_norm["season"] == basisjahr]["fg3a_per_fga_pct"].values[0]
        
        fg3_norm["fg3_norm"] = fg3_norm["fg3_pct"] / fg3_basiswert * 100
        fg3a_norm["fg3a_norm"] = fg3a_norm["fg3a_per_fga_pct"] / fg3a_basiswert * 100
        
        if player_name:
            player_fg3_norm = player_fg3_by_season.copy()
            player_fg3a_norm = player_fg3a_by_season.copy()
            player_fg3_norm["fg3_norm"] = player_fg3_norm["fg3_pct"] / fg3_basiswert * 100
            player_fg3a_norm["fg3a_norm"] = player_fg3a_norm["fg3a_per_fga_pct"] / fg3a_basiswert * 100

    apply_dark_theme()

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(12, 6))

    if normalisiert:
        sns.lineplot(data=fg3_norm, x="season", y="fg3_norm", marker="o", linewidth=2, label="FG3% (normiert)", ax=ax)
        if zeige_fg3a:
            sns.lineplot(data=fg3a_norm, x="season", y="fg3a_norm", marker="o", linewidth=2, label="FG3A/FGA% (normiert)", ax=ax)
        if player_name:
            sns.lineplot(data=player_fg3_norm, x="season", y="fg3_norm", marker="o", linewidth=2, label=f"{player_name} FG3% (normiert)", ax=ax)
            if zeige_fg3a:
                sns.lineplot(data=player_fg3a_norm, x="season", y="fg3a_norm", marker="o", linewidth=2, label=f"{player_name} FG3A/FGA% (normiert)", ax=ax)
        ax.axhline(100, color="gray", linestyle="--", linewidth=1)
        ax.set_ylabel("Index (Basisjahr = 100)")
    else:
        sns.lineplot(data=fg3_by_season, x="season", y="fg3_pct", marker="o", linewidth=2, label="Ligadurchschnitt FG3%", ax=ax)
        if zeige_fg3a:
            sns.lineplot(data=fg3a_share_by_season, x="season", y="fg3a_per_fga_pct", marker="o", linewidth=2, label="Ligadurchschnitt FG3A/FGA%", ax=ax)
        if player_name:
            sns.lineplot(data=player_fg3_by_season, x="season", y="fg3_pct", marker="o", linewidth=2, label=f"{player_name} FG3%", ax=ax)
            if zeige_fg3a:
                sns.lineplot(data=player_fg3a_by_season, x="season", y="fg3a_per_fga_pct", marker="o", linewidth=2, label=f"{player_name} FG3A/FGA%", ax=ax)
        ax.set_ylabel("FG3% / FG3A-FG Anteil")

    
    # Plot anpassen
    ax.set_title("Historische Entwicklung der Dreierwürfe – Liga vs. Spieler")
    ax.set_xlabel("Saisonjahr")
    ax.set_ylabel("FG3%")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    # Plot anzeigen
    st.pyplot(fig)

    st.markdown("""
        <div style='padding: 1rem; background-color: #1f2633; border-radius: 0.5rem; color: white;'>
        <b>Analyseergebnis:</b>   <br><br>
        Aus der Analyse geht hervor, dass die Trefferquote bei Dreipunktwürfen über die Jahre gestiegen ist,  
        jedoch nicht so stark wie der Anteil der tatsächlich ausgeführten Dreipunktwürfe am gesamten Wurfvolumen.       
        <br><br>
        🏀<b> Was geschah in der NBA-Saison 2015/2016?</b>
                
        Stephen Curry (Golden State Warriors) spielte eine historische Saison:<br><br>
        - Er wurde einstimmig zum MVP gewählt<br>
        - Er stellte einen Rekord mit 402 erfolgreichen Dreipunktwürfen auf (der vorherige Rekord lag bei 286!)
        Die Warriors spielten im Stil von „pace and space“ und setzten stark auf Dreierwürfe.<br><br>
        <b>Im Grunde begann mit der Saison 2016 die Ära des Dreipunkt-Basketballs:</b>   <br>
        Teams begannen massenhaft, ihre Anzahl an Dreierversuchen zu erhöhen.<br>
        📈 Auf den Grafiken mit fg3a_per_fga_pct sieht man einen deutlichen Sprung nach oben ab 2015.<br>
        Vorher stieg die Zahl der Dreier langsam, doch nach Curry und den Warriors wurde der Trend explosiv.


        </div>
        """, unsafe_allow_html=True)
