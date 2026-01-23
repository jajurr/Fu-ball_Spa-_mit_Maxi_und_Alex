import streamlit as st
import matplotlib.pyplot as plt
from db import query_df
from queries import Q_OWN_GOALS_SEASON, Q_OWN_GOALS_ALLTIME,  Q_TOP_OWN_GOAL_SCORERS_SEASON, Q_TOP_OWN_GOAL_SCORERS_ALLTIME

st.title("Eigentore")
liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])

mode = st.radio(
    "Zeitraum",
    ["Eine Saison", "Alle Saisons"],
    horizontal=True
)



if mode == "Eine Saison":
    limit = st.slider("Max. Anzahl Zeilen", min_value=5, max_value=50, value=5, step=5)
    saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2025, step=1)
    df = query_df(Q_OWN_GOALS_SEASON, (liga, saison))
else:
    limit = st.slider("Max. Anzahl Zeilen", min_value=5, max_value=400, value=50, step=5)
    df = query_df(Q_OWN_GOALS_ALLTIME, (liga,))

if df.empty:
    st.warning("Keine Eigentore gefunden/Daten fehlen.")
    st.stop()

total_own_goals = len(df)

st.metric(
    label="Anzahl Eigentore",
    value=total_own_goals
)

st.metric("Anzahl Eigentore", len(df))

# Minute hübsch: NULL -> —
df_disp = df.copy()
df_disp["Spielminute"] = df_disp["Spielminute"].apply(lambda x: "—" if x is None else int(x))

# ggf. limit anwenden
df_disp = df_disp.head(int(limit))

st.dataframe(df_disp, use_container_width=True, hide_index=True)

st.divider()

top_df = None
if mode == "Eine Saison":
    pass
else:
    #Tabelle
    st.subheader("Die meisten Eigentore nach Spieler für alle Saisons")
    top_n = st.slider("Anzahl Spieler", min_value=5, max_value=50, value=10, step=5)       
    top_df = query_df(Q_TOP_OWN_GOAL_SCORERS_ALLTIME, (liga, int(top_n)))

    #Diagramm
    fig = plt.figure()
    plot_df = top_df.iloc[::-1]
    plt.barh(plot_df["Spieler"], plot_df["Eigentore"])
    plt.xlabel("Eigentore")
    plt.ylabel("Spieler")
    plt.grid(True)
    st.pyplot(fig, clear_figure=True)





