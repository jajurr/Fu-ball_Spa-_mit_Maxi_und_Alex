import streamlit as st
from db import query_df
from queries import Q_TEAMS_IN_LEAGUE_SEASON, Q_MATCHES_OF_TEAM_SEASON

st.title("Teams")
st.write("Wähle Liga und Saison, dann ein Team. Du bekommst alle Spiele (inkl. Ergebnis und MatchID).")

# Filter
liga = st.selectbox("Liga", ["Bundesliga", "Zweite Bundesliga"])
saison = st.number_input("Saison", min_value=2001, max_value=2030, value=2022, step=1)

teams = query_df(Q_TEAMS_IN_LEAGUE_SEASON, (liga, saison))

if teams.empty:
    st.warning("Keine Teams gefunden. Prüfe LigaName/Saison oder ob MannschaftSpieltInLiga gefüllt ist.")
    st.stop()

team_name = st.selectbox("Team", teams["Name"].tolist())
team_id = int(teams.loc[teams["Name"] == team_name, "TeamID"].iloc[0])

matches = query_df(Q_MATCHES_OF_TEAM_SEASON, (liga, saison, team_id, team_id))

st.subheader(f"Spiele von {team_name} ({liga}, Saison {saison})")

if matches.empty:
    st.warning("Keine Spiele gefunden. Prüfe, ob Spiel + MannschaftSpieltSpiel korrekt importiert wurden.")
    st.stop()

# Ergebnis-Spalte hübsch zusammenbauen
def format_result(row):
    if row["HeimTore"] is None or row["GastTore"] is None:
        return "—"
    return f"{int(row['HeimTore'])}:{int(row['GastTore'])}"

matches_display = matches.copy()
matches_display["Ergebnis"] = matches_display.apply(format_result, axis=1)

# Nur die Spalten anzeigen, die Nutzer wirklich brauchen
matches_display = matches_display[["Spieltag", "Heimteam", "Gastteam", "Ergebnis", "MatchID"]]

st.dataframe(matches_display, use_container_width=True, hide_index=True)

st.divider()

# Optional: MatchID direkt "übernehmen" für Match-Detail-View
st.subheader("MatchID auswählen (für Match-Detail)")
match_id = st.selectbox("MatchID", matches_display["MatchID"].tolist())
st.session_state["selected_match_id"] = int(match_id)

st.info(
    f"Ausgewählte MatchID: {match_id}\n\n"
    "Tipp: Wir können als nächstes die Match-Detail-View so bauen, dass sie diese MatchID automatisch übernimmt."
)