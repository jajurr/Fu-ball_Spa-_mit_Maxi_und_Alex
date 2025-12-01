from api.openliga import get_bundesliga_teams, get_historische_saisons, get_spiele_einer_saison
from db.database import insert_team, insert_mannschaft_spielt_in_liga, insert_spiel, insert_mannschaft_spielt_spiel, insert_ergebnis

def import_teams_historisch():
    """Importiert alle Teams ab 2001 in die Mannschaft-Tabelle"""
    saisons = get_historische_saisons()
    for season in saisons:
        teams = get_bundesliga_teams(season)
        for t in teams:
            team_tuple = (t["teamId"], t["teamName"])
            insert_team(team_tuple)

def import_mannschaft_spielt_in_liga():
    """Befüllt die Zwischentabelle: jede Saison einzeln"""
    liga_name = "Bundesliga"
    saisons = get_historische_saisons()
    for season in saisons:
        teams = get_bundesliga_teams(season)
        for t in teams:
            eintrag = (
                season,       # Saison
                liga_name,    # Liga
                t["teamId"]   # Team
            )
            insert_mannschaft_spielt_in_liga(eintrag)

def import_spiele_saison(liga, saison):
    """
    Importiert alle Spiele einer Saison in die Datenbank.
    """
    spiele = get_spiele_einer_saison(liga, saison)

    for spiel in spiele:

        # -------------------- BASISDATEN --------------------
        match_id = spiel["matchID"]
        date_time = spiel["matchDateTime"]

        # Ort extrahieren (manchmal ist kein Ort angegeben)
        ort = None
        if "location" in spiel and spiel["location"] is not None:
            ort = spiel["location"].get("locationCity")

        insert_spiel(match_id, date_time, ort)

        # ---------------- HEIM- UND GASTMANNSCHAFT ----------------
        heim = spiel["team1"]["teamId"]
        gast = spiel["team2"]["teamId"]

        insert_mannschaft_spielt_spiel(match_id, heim, gast)

        # -------------------- ERGEBNIS -------------------------
        for erg in spiel["matchResults"]:
            ergebnis_id = erg["resultID"]
            heim_tore = erg["pointsTeam1"]
            gast_tore = erg["pointsTeam2"]

            is_halbzeit = (erg["resultTypeID"] == 1)

            insert_ergebnis(
                ergebnis_id,
                match_id,
                gast_tore,
                heim_tore,
                1 if is_halbzeit else 0
            )
