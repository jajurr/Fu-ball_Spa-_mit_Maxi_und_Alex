import streamlit as st
import matplotlib.pyplot as plt

from db import query_df
from queries import Q_CHAMPIONS_BY_SEASON

st.title("Meisterschaften")

liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])

df = query_df(Q_CHAMPIONS_BY_SEASON, (liga, liga))

if df.empty:
    st.warning("Keine Daten gefunden.")
    st.stop()

st.subheader("Meister je Saison")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

st.subheader("Häufigste Meister")
counts = df["Meister"].value_counts().reset_index()
counts.columns = ["Mannschaft", "Meisterschaften"]

st.dataframe(counts, use_container_width=True, hide_index=True)

fig = plt.figure()
plt.barh(counts["Mannschaft"][::-1], counts["Meisterschaften"][::-1])
plt.xlabel("Meisterschaften")
plt.ylabel("Team")
plt.grid(True)
st.pyplot(fig, clear_figure=True)