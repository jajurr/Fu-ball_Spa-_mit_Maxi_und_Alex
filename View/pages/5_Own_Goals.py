import streamlit as st
from db import query_df
from queries import Q_OWN_GOALS_SEASON, Q_OWN_GOALS_ALLTIME

st.title("Eigentore")
st.write("Alle Eigentore aus deiner SQLite-Datenbank (mit Filter nach Liga/Saison).")

liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])

mode = st.radio(
    "Zeitraum",
    ["Eine Saison", "Alle Saisons"],
    horizontal=True
)

limit = st.slider("Max. Anzahl Zeilen", min_value=5, max_value=100, value=5, step=5)

if mode == "Eine Saison":
    saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2022, step=1)
    df = query_df(Q_OWN_GOALS_SEASON, (liga, saison))
else:
    df = query_df(Q_OWN_GOALS_ALLTIME, (liga,))

if df.empty:
    st.warning("Keine Eigentore gefunden (oder Daten fehlen).")
    st.stop()

# Minute hübsch: NULL -> —
df_disp = df.copy()
df_disp["Spielminute"] = df_disp["Spielminute"].apply(lambda x: "—" if x is None else int(x))

# ggf. limit anwenden
df_disp = df_disp.head(int(limit))

st.dataframe(df_disp, use_container_width=True, hide_index=True)

st.caption("Tipp: MatchID kannst du in der Match-Detail-View verwenden.")