import streamlit as st
import matplotlib.pyplot as plt

def set_app_config(title: str, icon: str = "📊", layout: str = "wide"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout
    )

def load_custom_css(path="nba_dark_style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    print("🔵 CSS wurde geladen.")    

def apply_dark_theme():
    """Wendet die Einstellungen des dunklen Themas auf das aktuelle Diagramm an"""
    plt.rcParams.update({
        'figure.facecolor': '#0E1117',
        'axes.facecolor': '#0E1117',
        'axes.edgecolor': 'white',
        'axes.labelcolor': 'white',
        'text.color': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'grid.color': 'grey',
        'lines.linewidth': 1.5,
        'axes.linewidth': 1.5,
        'grid.linewidth': 0.8,
    })