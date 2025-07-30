import streamlit as st
from style_utils import set_app_config, show_sidebar_info, load_custom_css
import pandas as pd
import numpy as np
import joblib
import altair as alt
from pathlib import Path
import re
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import percentileofscore

set_app_config(
    title="ML",
    icon="📈",
    layout="wide"
)
show_sidebar_info()
load_custom_css()

st.markdown('<div class="centered-title">Vorhersagemodell</div>',
            unsafe_allow_html=True)

# ------------------------------------------------------------------
# 1) Load trained models (cached)
# ------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_models():
    """Load pre-trained models for Big, Guard and Wing."""
    return {
        lbl: joblib.load(f"data/best_model_{lbl}.pkl")
        for lbl in ("Big", "Guard", "Wing")
        if Path(f"data/best_model_{lbl}.pkl").exists()
    }

models = load_models()
if not models:
    st.error("❌ Keine Modelle gefunden. Bitte Training durchführen.")
    st.stop()

# Dataframe ---------------------------------------------------------------
df = pd.read_pickle("data/1_dataset_ML.pkl")

# Mapping & feature list ------------------------------------------------------
targets = {"Big": "score_big", "Guard": "score_guard", "Wing": "score_wing"}
feature_cols = [
    "height", "weight", "bmi", "draft_flag", "draft_age", "draft_number", "draft_group",
    "stand_jump", "max_jump", "court_sprint", "lane_agility", "bench_press"
]

# ------------------------------------------------------------------
# 2) Tabs – Success Score + Analysen
# ------------------------------------------------------------------
TABS = st.tabs([
    "Success Score", "Spielerwerte", "Busts & Steals"
])

# 2a – Success Score (Spieler‑Input) -----------------------------------------
with TABS[0]:
    col_input, col_space, col_balken = st.columns([14, 1, 5])

    with col_input:
        st.write("### ⭐ Vorhersage des Success Scores")
        st.info("ℹ️ Gib die Basisdaten eines Spielers ein, um seinen langfristigen Success Score vorherzusagen und mit ähnlichen Spielern zu vergleichen.")
        st.markdown("#### 🏀 Physische Attribute")

        # --- Physische Attribute ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            position = st.selectbox("Position", list(models.keys()))
        with col2:
            HEIGHT = st.slider("Größe (cm)", 160, 230, 200)
            DRAFT_AGE = 0  # wird unten gesetzt, falls Spieler drafted
        with col3:
            WEIGHT = st.slider("Gewicht (kg)", 60, 150, 100)
            DRAFT_NUM = 0
        with col4:
            BMI_val = WEIGHT / ((HEIGHT / 100) ** 2)
            st.markdown(f"BMI (kg/m²): {BMI_val:.1f}")
            st.caption("ℹ️ BMI wird automatisch berechnet.")
        st.markdown("---")

        # --- Draft Infos ---
        st.markdown("#### 🏆 Draft Infos")
        DRAFT_FLAG = st.checkbox("Drafted?", value=False)
        DRAFT_GRP = 7  # Standard: undrafted

        if DRAFT_FLAG:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                DRAFT_NUM = st.slider("Draft Nummer", 1, 60, 1)
            with col_d2:
                DRAFT_AGE = st.slider("Draft Alter", 18, 30, 21)

            # Automatische Gruppenzuordnung
            if 1 <= DRAFT_NUM <= 10:
                DRAFT_GRP = 1
            elif 11 <= DRAFT_NUM <= 20:
                DRAFT_GRP = 2
            elif 21 <= DRAFT_NUM <= 30:
                DRAFT_GRP = 3
            elif 31 <= DRAFT_NUM <= 40:
                DRAFT_GRP = 4
            elif 41 <= DRAFT_NUM <= 50:
                DRAFT_GRP = 5
            else:
                DRAFT_GRP = 6
        else:
            # Spieler undrafted
            DRAFT_NUM = 0
            DRAFT_AGE = 0
            DRAFT_GRP = 7

        st.caption("ℹ️ Draft-Gruppe wird automatisch aus der Draft Number bestimmt (1=Top10, 2=11–20, …, 7=Undrafted).")
        st.markdown("---")

        # --- Combine Werte ---
        st.markdown("#### 🏋️ Combine Werte")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            SJUMP = st.number_input("Standing Jump (cm)", 0.0, 50.0, 29.5, step=0.1, format="%.1f")
        with c2:
            MJUMP = st.number_input("Max Jump (cm)", 0.0, 50.0, 35.0, step=0.1, format="%.1f")
        with c3:
            SPRINT = st.number_input("Court Sprint (s)", 2.0, 4.0, 3.25, step=0.01, format="%.2f")
        with c4:
            AGILITY = st.number_input("Lane Agility (s)", 8.0, 15.0, 11.3, step=0.01, format="%.2f")
        with c5:
            BENCH = st.number_input("Bench Press (Wdh)", 0, 30, 10)
        # --- Styling für Button ---
        st.markdown("""
            <style>
            div.stButton > button {
                height: 60px;
                width: 300px;
                font-size: 20px; 
                margin-top: 10px;
            }
            </style>
            """, unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 1])
        with col_btn2:
            predict_btn = st.button("🔮 Score vorhersagen")

    # -----------------------------
    # Prediction Input Dictionary
    # -----------------------------
    user_input = {
        "height": [HEIGHT],
        "weight": [WEIGHT],
        "bmi": [round(BMI_val, 1)],
        "draft_age": [DRAFT_AGE],
        "draft_number": [DRAFT_NUM],
        "draft_group": [DRAFT_GRP],
        "draft_flag": [1 if DRAFT_FLAG else 0],
        "stand_jump": [round(SJUMP, 1)],
        "max_jump": [round(MJUMP, 1)],
        "court_sprint": [round(SPRINT, 2)],
        "lane_agility": [round(AGILITY, 2)],
        "bench_press": [round(BENCH, 0)]
    }

# ------------------------------------------------------------------
# 3) Prediction
# ------------------------------------------------------------------
user_input = {
    "height": [HEIGHT], "weight": [WEIGHT], "bmi": [round(BMI_val, 2)],
    "draft_age": [DRAFT_AGE], "draft_number": [DRAFT_NUM], "draft_group": [DRAFT_GRP],
    "stand_jump": [SJUMP], "max_jump": [MJUMP], "court_sprint": [SPRINT],
    "lane_agility": [AGILITY], "bench_press": [BENCH], "draft_flag": [1 if DRAFT_FLAG else 0]
}

with col_balken:
    st.markdown(f"### 📈 Predicted Success Score ({position}s)")
    if predict_btn:

        # Berechne prediction
        X_user = pd.DataFrame(user_input)
        score_pred = models[position].predict(X_user)[0]

        score_col = targets.get(position)

        percentile = None
        if score_col and not df.empty:
            scores_pos = df[df["pos_cluster"] == position][score_col].dropna()
            if not scores_pos.empty:
                percentile = percentileofscore(scores_pos, score_pred, kind='weak')

        # Anzeige der Prediction als Text über dem Diagramm
        st.markdown(
            f"<div style='text-align:center; font-size:3rem; color: white;'>{score_pred:.1f}</div>",
            unsafe_allow_html=True,
        )

        df_filtered = df[df["pos_cluster"] == position]
        score_col = targets.get(position)

        if score_col and not df_filtered.empty:
            min_score = df_filtered[score_col].min()
            max_score = df_filtered[score_col].max()
        else:
            min_score = 0
            max_score = 100

        # Hintergrundbalken (Score-Bereich)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Score"],
            y=[max_score - min_score],
            base=min_score,
            width=0.4,
            marker=dict(color="gray", opacity=0.3),
            hoverinfo="skip",
            showlegend=False
        ))

        # Rote Linie quer über den Balken
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=0.5,
            y0=score_pred,
            y1=score_pred,
            line=dict(color="#FF4B4B", width=3)
        )

        # Textlabel direkt an der Linie
        fig.add_annotation(
            x=0,
            y=score_pred,
            text=f"{score_pred:.1f} ({percentile:.0f}. Perzentil)",
            showarrow=False,
            font=dict(color="white", size=14),
            yshift=10
        )

        # Min-Score Annotation
        fig.add_annotation(
            x=0,
            y=min_score,
            text=f"Min: {min_score:.1f}",
            showarrow=False,
            font=dict(color="white", size=14),
            yshift=-20
        )

        # Max-Score Annotation
        fig.add_annotation(
            x=0,
            y=max_score,
            text=f"Max: {max_score:.1f}",
            showarrow=False,
            font=dict(color="white", size=14),
            yshift=10
        )

        # Layout – schwarz & weiß
        fig.update_layout(
            height=650,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            margin=dict(l=10, r=10, t=30, b=30),
            yaxis=dict(
                range=[min_score - 5, max_score + 5],
                tickfont=dict(color="white"),
                title=dict(
                    text="Score",
                    font=dict(color="white")
                )
            ),
            xaxis=dict(
                showticklabels=False
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 4) Analysis Tabs ------------------------------------------------------------
# ------------------------------------------------------------------

# 4a – Spielerwerte -----------------------------------------------------
with TABS[1]:
    # Relativer Vergleich der Metriken
    st.write(f"### 📊 Spielerwerte im Positionsvergleich mit {position}s")
    st.info("ℹ️ Vergleich der Attribute eines Spielers mit den Min- und Max-Werten seiner Positionsgruppe (grauer Balken) und Markierung seines eigenen Werts (rote Linie) inkl. Perzentil.")

    # Spalten, die nicht angezeigt werden sollen
    exclude_features = ["draft_group", "draft_flag"]

    # Rundungsregeln pro Feature
    rounding_rules = {
        "height": 0,
        "weight": 0,
        "draft_age": 0,
        "draft_number": 0,
        "bench_press": 0,
        "bmi": 1,
        "max_jump": 1,
        "stand_jump": 1,
        "court_sprint": 2,
        "lane_agility": 2
        }

    df_pos = df[df["pos_cluster"] == position]
    
    # --- Kategorien ---
    categories = {
        "🏀 Physische Attribute": ["height", "weight", "bmi"],
        "🏆 Draft Infos": ["draft_age", "draft_number"],
        "🏋️ Combine Werte": ["stand_jump", "max_jump", "court_sprint", "lane_agility", "bench_press"]
    }

    # --- Plotbeschriftungen ---
    title_map = {
        "height": "Größe (cm)",
        "weight": "Gewicht (kg)",
        "bmi": "BMI (kg/m²)",
        "draft_age": "Draft Alter",
        "draft_number": "Draft Nummer",
        "stand_jump": "Standing Jump (cm)",
        "max_jump": "Max Jump (cm)",
        "court_sprint": "Court Sprint (s)",
        "lane_agility": "Lane Agility (s)",
        "bench_press": "Bench Press (Wdh)"
    }

    for cat_name, cat_features in categories.items():
        # Filter nur Features, die existieren
        cat_features = [f for f in cat_features if f in df_pos.columns and f in user_input.keys()]

        if not cat_features:
            continue

        # Miniüberschrift
        st.markdown(f"#### {cat_name}")

        # Zeilenweise Darstellung mit max 3 Plots
        cols_per_row = 3
        rows = (len(cat_features) + cols_per_row - 1) // cols_per_row

        for r in range(rows):
            cols = st.columns(cols_per_row)
            for i, feature in enumerate(cat_features[r*cols_per_row:(r+1)*cols_per_row]):
                user_val = float(np.ravel(user_input[feature])[0]) if isinstance(user_input[feature], (list, np.ndarray)) else float(user_input[feature])
                data_series = df_pos[feature].dropna()

                # --- Sonderfälle ---
                if feature == "draft_age":
                    data_series = data_series[data_series > 0]
                    min_score = max(18, data_series.min()) if not data_series.empty else 18
                else:
                    min_score = data_series.min() if not data_series.empty else 0

                if feature == "draft_number":
                    if user_val == 0:
                        user_val = 61
                    data_series = data_series.apply(lambda x: 61 if x == 0 else x)
                    max_score = 60
                else:
                    max_score = data_series.max() if not data_series.empty else user_val

                decimals = rounding_rules.get(feature, 2)
                min_fmt = f"{min_score:.{decimals}f}"
                max_fmt = f"{max_score:.{decimals}f}"
                user_fmt = f"{user_val:.{decimals}f}"

                percentile = None
                if not data_series.empty:
                    if feature in ["draft_number", "court_sprint", "lane_agility"]:
                        perc = percentileofscore(data_series, user_val, kind='weak')
                        percentile = 100 - perc
                    else:
                        percentile = percentileofscore(data_series, user_val, kind='weak')

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=[feature],
                    y=[max_score - min_score],
                    base=min_score,
                    width=0.4,
                    marker=dict(color="gray", opacity=0.3),
                    hoverinfo="skip",
                    showlegend=False
                ))

                if not (feature in ["draft_number", "draft_age"] and user_input["draft_flag"] == [0]):
                    fig.add_shape(
                        type="line",
                        x0=-0.5,
                        x1=0.5,
                        y0=user_val,
                        y1=user_val,
                        line=dict(color="#FF4B4B", width=3)
                    )

                    perc_text = f"{user_fmt}"
                    if percentile is not None:
                        perc_text += f" ({percentile:.0f}%)"

                    fig.add_annotation(
                        x=0,
                        y=user_val,
                        text=perc_text,
                        showarrow=False,
                        font=dict(color="white", size=14),
                        yshift=10
                    )

                fig.add_annotation(
                    x=0,
                    y=min_score,
                    text=f"Min: {min_fmt}",
                    showarrow=False,
                    font=dict(color="white", size=12),
                    yshift=-20
                )
                fig.add_annotation(
                    x=0,
                    y=max_score,
                    text=f"Max: {max_fmt}",
                    showarrow=False,
                    font=dict(color="white", size=12),
                    yshift=10
                )

                fig.update_layout(
                    height=300,
                    plot_bgcolor="#0E1117",
                    paper_bgcolor="#0E1117",
                    margin=dict(l=120, r=120, t=100, b=20),
                    yaxis=dict(
                        range=[min_score - (0.05 * abs(max_score)), max_score + (0.05 * abs(max_score))],
                        tickfont=dict(color="white"),
                        title=None  # y-Achsenbeschriftung entfernen
                    ),
                    xaxis=dict(showticklabels=False),
                    title=dict(
                        text=title_map.get(feature, feature.replace("_", " ").title()),
                        font=dict(color="white", size=14),
                        x=0.5,                 # zentriert (0=links, 0.5=Mitte, 1=rechts)
                        xanchor="center",      # Ankerpunkt in der Mitte
                        yanchor="top"
                    ),
                    showlegend=False
                )

                cols[i].plotly_chart(fig, use_container_width=True)
        st.markdown("---")  # Trennlinie nach jeder Kategorie

# 4b – Busts & Steals ---------------------------------------------------------
with TABS[2]:
    st.write("### ⚖️ Bust or Steal?")
    st.info("ℹ️ Vergleich des vorhergesagten und tatsächlichen Success Scores für einen ausgewählten Spieler und Übersicht der Top Busts und Steals.")

    col = targets[position]
    y_true  = df[col].dropna()
    X_hold  = df.loc[y_true.index, feature_cols]
    players = df.loc[y_true.index, "player"]

    y_pred  = models[position].predict(X_hold)
    errors  = np.round(y_true.values - y_pred, 1)

    df_err  = pd.DataFrame(
        {
            "player": players.values,
            "error": errors,
            "true": np.round(y_true.values, 1),
            "pred": np.round(y_pred, 1),
        }
    )

    # Manuelle Spielerauswahl
    st.write("#### 🎯 Individuelle Spieleranalyse") 

    player_list = ["--- Spieler wählen ---"] + sorted(df_err["player"].unique())
    selected_player = st.selectbox(
        label="",
        options=player_list,
        index=0,
        label_visibility="collapsed"
    )

    if selected_player != "--- Spieler wählen ---":
        player_data = df_err[df_err["player"] == selected_player].iloc[0]
        player_true = player_data["true"]
        player_pred = player_data["pred"]
        player_error = player_data["error"]

        # Positionscluster des ausgewählten Spielers
        selected_cluster = df[df["player"] == selected_player]["pos_cluster"].iloc[0]
        score_col = targets.get(selected_cluster)

        # Cluster-Werte nur für Spieler dieser Position
        cluster_scores = df[df["pos_cluster"] == selected_cluster][score_col].dropna()

        min_cluster = cluster_scores.min() if not cluster_scores.empty else min(player_true, player_pred)
        max_cluster = cluster_scores.max() if not cluster_scores.empty else max(player_true, player_pred)

        # Bewertung
        if player_error > 3:
            rating = "💎 Steal"
        elif player_error < -3:
            rating = "🚫 Bust"
        else:
            rating = "🔘 Neutral"

        # Balkendiagramm
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Score"],
            y=[max_cluster - min_cluster],
            base=min_cluster,
            width=0.4,
            marker=dict(color="gray", opacity=0.3),
            hoverinfo="skip",
            showlegend=False
        ))

        # Linie für Prognose
        fig.add_shape(
            type="line",
            x0=-0.5, x1=0.5,
            y0=player_pred, y1=player_pred,
            line=dict(color="#FF4B4B", width=3),
            name="Prognose"
        )
        fig.add_annotation(
            x=0,
            y=player_pred,
            text=f"Pred: {player_pred:.1f}",
            showarrow=False,
            font=dict(color="white", size=12),
            yshift=12
        )

        # Linie für Tatsächlich
        fig.add_shape(
            type="line",
            x0=-0.5, x1=0.5,
            y0=player_true, y1=player_true,
            line=dict(color="#4CAF50", width=3),
            name="Tatsächlich"
        )
        fig.add_annotation(
            x=0,
            y=player_true,
            text=f"True: {player_true:.1f}",
            showarrow=False,
            font=dict(color="white", size=12),
            yshift=-15
        )

        # Min-Wert
        fig.add_annotation(
            x=0,
            y=min_cluster,
            text=f"Min: {min_cluster:.1f}",
            showarrow=False,
            font=dict(color="white", size=12),
            yshift=-20
        )

        # Max-Wert
        fig.add_annotation(
            x=0,
            y=max_cluster,
            text=f"Max: {max_cluster:.1f}",
            showarrow=False,
            font=dict(color="white", size=12),
            yshift=10
        )

        # Layout
        fig.update_layout(
            height=300,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            margin=dict(l=200, r=200, t=30, b=30),
            yaxis=dict(
                range=[min_cluster - 5, max_cluster + 5],
                tickfont=dict(color="white"),
                title=dict(
                    text="Success Score",
                    font=dict(color="white")
                )
            ),
            xaxis=dict(showticklabels=False),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Textausgabe
        st.write(f"**Abweichung:** {player_error:.1f}")
        st.write(f"**Bewertung:** {rating}")
    st.markdown("---")


    # Top 5 Charts
    busts  = df_err.nlargest(5, "error")
    steals = df_err.nsmallest(5, "error")

    st.write("#### 💎 Top 5 Steals")
    bust_chart = (
        alt.Chart(busts)
        .mark_bar(color="green")
        .encode(
            x=alt.X("error:Q", title="Abweichung (True - Pred)"),
            y=alt.Y("player:N", sort="-x", title=""),
            tooltip=["player", "true", "pred", "error"],
        )
        .properties(height=300)
    )
    st.altair_chart(bust_chart, use_container_width=True)

    st.write("#### 🚫 Top 5 Busts")
    steal_chart = (
        alt.Chart(steals)
        .mark_bar(color="red")
        .encode(
            x=alt.X("error:Q", title="Abweichung (True - Pred)"),
            y=alt.Y("player:N", sort="x", title=""),
            tooltip=["player", "true", "pred", "error"],
        )
        .properties(height=300)
    )
    st.altair_chart(steal_chart, use_container_width=True)