import streamlit as st
import matplotlib.pyplot as plt

from db import query_df
from queries import Q_GOALS_PER_MATCHDAY, Q_KPIS


st.title("Overview")
st.write("Saisonübersicht: Kennzahlen und Tore pro Spieltag.")

# Sidebar / Filter
liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])
saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2022, step=1)

# KPIs laden
kpis = query_df(Q_KPIS, (liga, saison, liga, saison, liga, saison))

col1, col2, col3 = st.columns(3)
col1.metric("Spiele", int(kpis.loc[0, "Spiele"]) if not kpis.empty else 0)
col2.metric("Tore", int(kpis.loc[0, "Tore"]) if not kpis.empty else 0)
col3.metric("Eigentore", int(kpis.loc[0, "Eigentore"]) if not kpis.empty else 0)

st.divider()

# Tore pro Spieltag
df = query_df(Q_GOALS_PER_MATCHDAY, (liga, saison))

st.subheader("Tore pro Spieltag")
if df.empty:
    st.warning("Keine Daten gefunden. Prüfe Liga/Saison oder ob der Import vollständig ist.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = plt.figure()
    plt.plot(df["Spieltag"], df["Tore"], marker="o")
    plt.xlabel("Spieltag")
    plt.ylabel("Tore")
    plt.grid(True)
    st.pyplot(fig, clear_figure=True)