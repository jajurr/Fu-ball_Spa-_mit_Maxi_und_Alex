import streamlit as st
from db import query_df, blob_to_bytes
from queries import (
    Q_MATCH_HEADER,
    Q_MATCH_ENDRESULT,
    Q_MATCH_HALFTIME,
    Q_MATCH_GOALS
)

st.title("Spiel Details")
default_match_id = st.session_state.get("selected_match_id", 39738)

match_id = st.number_input(
    "MatchID",
    min_value=1,
    value=int(default_match_id),
    step=1
)

header = query_df(Q_MATCH_HEADER, (int(match_id),))

if header.empty:
    st.error(f"Kein Spiel mit der MatchID {match_id} gefunden.")
    st.stop()

h = header.iloc[0]

st.subheader(f"{h['Heimmannschaft']} vs. {h['Gastmannschaft']}")

heim_logo = blob_to_bytes(h["HeimLogo"])
gast_logo = blob_to_bytes(h["GastLogo"])

saison_txt = int(h["Saison"]) if h["Saison"] is not None else "—"
spieltag_txt = int(h["Spieltag"]) if h["Spieltag"] is not None else "—"

c_logo_l, c_team_l, c_mid, c_team_r, c_logo_r = st.columns([1, 3, 2, 3, 1])

with c_logo_l:
    if heim_logo:
        st.image(heim_logo, width=90)

with c_team_l:
    st.header(h["Heimmannschaft"])

with c_mid:
    st.write("")
    st.write("")
    st.subheader("VS")
    st.caption(f"Saison {saison_txt} · Spieltag {spieltag_txt}")

with c_team_r:
    st.header(h["Gastmannschaft"])

with c_logo_r:
    if gast_logo:
        st.image(gast_logo, width=90)


left, mid, right = st.columns(3)
left.metric("Saison", int(h["Saison"]) if h["Saison"] is not None else "—")
mid.metric("Spieltag", int(h["Spieltag"]) if h["Spieltag"] is not None else "—")
right.metric("Ort", h["Ort"] if h["Ort"] else "—")

if h["MatchDateTime"]:
    st.caption(f"Anstoß: {h['MatchDateTime']}")

endres = query_df(Q_MATCH_ENDRESULT, (int(match_id),))
half = query_df(Q_MATCH_HALFTIME, (int(match_id),))

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Endergebnis")
    if endres.empty:
        st.write("—")
    else:
        e = endres.iloc[0]
        st.write(f"**{int(e['HeimTore'])}:{int(e['GastTore'])}**")

with col2:
    st.markdown("### Halbzeit")
    if half.empty:
        st.write("—")
    else:
        hz = half.iloc[0]
        st.write(f"**{int(hz['HeimTore'])}:{int(hz['GastTore'])}**")

st.divider()

st.subheader("Tore")

goals = query_df(Q_MATCH_GOALS, (int(match_id), int(match_id)))

if goals.empty:
    st.info("Keine Tore gespeichert (oder keine Spieler-Namen vorhanden).")
else:
    goals_disp = goals.copy()
    goals_disp["Minute"] = goals_disp["Spielminute"].apply(lambda x: "—" if x == 999 else int(x))
    goals_disp["Mannschaft"] = goals_disp["Mannschaft"].fillna("Unbekannt")

    def flags(row):
        parts = []
        if int(row["isPenalty"]) == 1:
            parts.append("Elfmeter")
        if int(row["isOwnGoal"]) == 1:
            parts.append("Eigentor")
        if int(row["isOvertime"]) == 1:
            parts.append("Overtime")
        return ", ".join(parts) if parts else ""

    goals_disp["Info"] = goals_disp.apply(flags, axis=1)

    goals_disp = goals_disp[["Minute", "Spieler", "Mannschaft", "Seite", "Info", "GoalID"]]

    st.dataframe(goals_disp, use_container_width=True, hide_index=True)