import streamlit as st

st.set_page_config(
    page_title="Fußball App",
    layout="wide"
)

st.title("Fußball App")
st.write(
    """
    Diese App liest Daten aus deiner SQLite-Datenbank (read-only) und stellt sie in mehreren Views dar.
    
    Links in der Navigation erscheinen später die Seiten (z.B. Overview, Teams, Match-Details, Top-Scorer, Eigentore).
    """
)

st.info(
    "Nächster Schritt: Wir erstellen die erste View in `pages/1_Overview.py`."
)