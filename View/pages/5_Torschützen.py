import streamlit as st
import matplotlib.pyplot as plt

from db import query_df
from queries import Q_TOP_SCORER_SEASON, Q_TOP_SCORER_ALLTIME

st.title("Torschützen")

liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])

mode = st.radio(
    "Zeitraum",
    ["Eine Saison", "Alle Saisons"],
    horizontal=True
)

if mode == "Eine Saison":
    top_n = st.slider("Anzahl Spieler", min_value=5, max_value=25, value=10, step=5)
    saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2025, step=1)
    df = query_df(Q_TOP_SCORER_SEASON, (liga, saison, int(top_n)))
else:
    top_n = st.slider("Anzahl Spieler", min_value=5, max_value=100, value=20, step=5)
    df = query_df(Q_TOP_SCORER_ALLTIME, (liga, int(top_n)))

if df.empty:
    st.warning("Keine Daten gefunden.")
    st.stop()

st.subheader("Tabelle")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Diagramm")

# Balkendiagramm
df_plot = df.iloc[::-1]  # umdrehen, damit Top1 oben steht

fig = plt.figure(figsize=(5, 3))
plt.tight_layout()
plt.barh(df_plot["Spieler"], df_plot["Tore"])
plt.xlabel("Tore")
plt.ylabel("Spieler")
plt.grid(True)
st.pyplot(fig, clear_figure=True)