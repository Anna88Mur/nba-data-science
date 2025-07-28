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
            <li>Boxplots z. B. Draftposition vs. PPG/All-Star-Status</li>
            <li>Streudiagramme (z. B. Minuten vs. Erfolg)</li>
        </ul>

</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["📈 Korrelationen", "📊 Draft-Analysen", "🔍 Dreipunktewurf-Analysen"])

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

    #Variante 1
    
    fig = px.imshow(
        corr_data,
        text_auto=".2f",
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1,
        aspect="auto",
        labels=dict(color="Korrelation")
    )
    
    fig.update_layout(
         title="Korrelationsmatrix",
         width=800,  # Feste Breite
         height=700, # Feste Höhe
         xaxis_title="",
         yaxis_title="",
         font=dict(size=10)
    )
    
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    #Variante 2
    #Figur erstellen
    plt.figure(figsize=(20, 16))
    sns.clustermap(corr_data, cmap="coolwarm", annot=True)

    plt.title("Korrelationsmatrix physischer und spielerischer Merkmale", fontsize=20)
    
    # Figur an Streamlit übergeben
    st.pyplot(plt.gcf())
    plt.clf()  # Aktuelle Figur löschen für nächste Plots



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


with tab2:
    st.header("📊 Draft-Analysen")
    


with tab3:
    st.header("🔍 Dreipunktewurf-Analysen")
     