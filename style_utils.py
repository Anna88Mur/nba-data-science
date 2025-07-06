import streamlit as st


def set_app_config(title: str, icon: str = "📊", layout: str = "wide"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout
    )


def show_sidebar_info():
    st.sidebar.title("📂 Navigation")
    st.sidebar.caption("⬆️ Seitenübersicht")
    st.sidebar.info("Wähle links eine Analyse.")


def load_custom_css(path="nba_dark_style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    print("🔵 CSS wurde geladen.")    
