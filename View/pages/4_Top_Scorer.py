import streamlit as st
import matplotlib.pyplot as plt

from db import query_df
from queries import Q_TOP_SCORER_SEASON, Q_TOP_SCORER_ALLTIME

st.title("Top Scorer")
st.write("Top-Torschützen (ohne Eigentore) aus deiner SQLite-Datenbank.")

liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])

mode = st.radio(
    "Zeitraum",
    ["Eine Saison", "Alle Saisons"],
    horizontal=True
)

top_n = st.slider("Wie viele Spieler anzeigen?", min_value=5, max_value=20, value=10, step=1)

if mode == "Eine Saison":
    saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2022, step=1)
    df = query_df(Q_TOP_SCORER_SEASON, (liga, saison, int(top_n)))
else:
    df = query_df(Q_TOP_SCORER_ALLTIME, (liga, int(top_n)))

if df.empty:
    st.warning("Keine Daten gefunden. Prüfe, ob Tore/Spieler importiert wurden und ob die LigaName-Werte passen.")
    st.stop()

st.subheader("Tabelle")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Diagramm")

# Balkendiagramm (oben: höchster Wert)
df_plot = df.iloc[::-1]  # umdrehen, damit Top1 oben steht

fig = plt.figure()
plt.barh(df_plot["Spieler"], df_plot["Tore"])
plt.xlabel("Tore")
plt.ylabel("Spieler")
plt.grid(True)
st.pyplot(fig, clear_figure=True)