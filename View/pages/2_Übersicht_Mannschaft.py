import streamlit as st
import pandas as pd 
from db import query_df
from queries import Q_TEAMS_IN_LEAGUE_SEASON, Q_MATCHES_OF_TEAM_SEASON


st.title("Mannschaftsübersicht")

# Filter
liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])
saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2025, step=1)

teams = query_df(Q_TEAMS_IN_LEAGUE_SEASON, (liga, saison))

if teams.empty:
    st.warning("Keine Teams gefunden.")
    st.stop()

team_name = st.selectbox("Team", teams["Name"].tolist())
team_id = int(teams.loc[teams["Name"] == team_name, "TeamID"].iloc[0])

matches = query_df(Q_MATCHES_OF_TEAM_SEASON, (liga, saison, team_id, team_id))

st.subheader(f"Spiele von {team_name} ({liga}, Saison {saison})")

if matches.empty:
    st.warning("Keine Spiele gefunden.")
    st.stop()

matches_display = matches.copy()

# HeimTore / GastTore robust behandeln
matches_display["HeimTore"] = pd.to_numeric(matches_display["HeimTore"], errors="coerce")
matches_display["GastTore"] = pd.to_numeric(matches_display["GastTore"], errors="coerce")

# Ergebnis bauen
matches_display["Ergebnis"] = (
    matches_display["HeimTore"].fillna(pd.NA).astype("Int64").astype(str)
    + ":"
    + matches_display["GastTore"].fillna(pd.NA).astype("Int64").astype(str)
)

# Spiele ohne Ergebnis explizit markieren
matches_display.loc[
    matches_display["HeimTore"].isna() | matches_display["GastTore"].isna(),
    "Ergebnis"
] = "—"

# Nur die Spalten anzeigen, die Nutzer wirklich brauchen
matches_display = matches_display[["Spieltag", "Heimteam", "Gastteam", "Ergebnis", "MatchID"]]

st.dataframe(matches_display, use_container_width=True, hide_index=True)

st.divider()

# Optional: MatchID direkt "übernehmen" für Match-Detail-View
st.subheader("MatchID auswählen (für Spiel Details)")
match_id = st.selectbox("MatchID", matches_display["MatchID"].tolist())
st.session_state["selected_match_id"] = int(match_id)