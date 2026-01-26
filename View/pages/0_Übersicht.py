import streamlit as st
import matplotlib.pyplot as plt

from db import query_df
from queries import Q_GOALS_PER_MATCHDAY, Q_KPIS, Q_TABLE_STANDINGS



st.title("Übersicht")

# Sidebar
liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])
saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2025, step=1)

st.subheader("Tabelle")
table_df = query_df(Q_TABLE_STANDINGS, (liga, saison, liga, saison))


table_df = query_df(Q_TABLE_STANDINGS, (liga, saison, liga, saison))
if table_df.empty:
    st.info("Keine Daten gefunden.")
else:
    table_display = table_df.copy()
    table_display.insert(0, "Platz", range(1, len(table_display) + 1))
    height = min(40 * (len(table_display) + 1), 800)
    st.dataframe(table_display, use_container_width=True, hide_index=True)

st.divider()

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
    st.warning("Keine Daten gefunden.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = plt.figure()
    plt.plot(df["Spieltag"], df["Tore"], marker="o")
    plt.xlabel("Spieltag")
    plt.ylabel("Tore")
    plt.grid(True)
    st.pyplot(fig, clear_figure=True)



