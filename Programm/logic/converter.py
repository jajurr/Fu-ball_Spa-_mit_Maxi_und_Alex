from api.openliga import get_bundesliga_teams, get_historische_saisons, get_spiele_einer_saison, get_goalgetters
from db.database import insert_team, insert_mannschaft_spielt_in_liga, insert_spiel, insert_mannschaft_spielt_spiel, insert_ergebnis, insert_spieler, insert_tor, insert_spieler_spielt_in_mannschaft, insert_spieler_schiesst_tor, update_spieler_name

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

def import_goalgetters_saison(liga, saison):
    data = get_goalgetters(liga, saison)
    for eintrag in data:
        spieler_id = eintrag["goalGetterId"]
        name = eintrag.get("goalGetterName")
        if name:
            update_spieler_name(spieler_id, name)

def import_spiele_saison(liga, saison):
    """
    Importiert alle Spiele einer Saison in die Datenbank.
    """
    spiele = get_spiele_einer_saison(liga, saison)

    for spiel in spiele:

        # -------------------- BASISDATEN --------------------
        match_id = spiel["matchID"]
        date_time = spiel["matchDateTime"]
        spieltag = spiel["group"]["groupOrderID"]

        # Ort extrahieren (manchmal ist kein Ort angegeben)
        ort = None
        if "location" in spiel and spiel["location"] is not None:
            ort = spiel["location"].get("locationCity")

        insert_spiel(match_id, date_time, ort, saison, spieltag)

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

        # -------------------- TORE IMPORTIEREN --------------------
        for tor in spiel.get("goals", []):
            goal_id = tor["goalID"]
            minute = tor.get("matchMinute")
            spieler_id = tor["goalGetterID"]
            spieler_name = tor["goalGetterName"]

            #Spieler ohne Namen werden ignoriert
            #if not spieler_name or spieler_name.strip() in ("", "0"):
            #   continue

            # 1) Spieler speichern                
            insert_spieler(spieler_id, spieler_name)

            # 2) Tor speichern
            insert_tor(goal_id, minute, match_id)

            # 3) SpielerSchiesstTor speichern
            insert_spieler_schiesst_tor(
                spieler_id,
                goal_id,
                1 if tor["isOwnGoal"] else 0,
                1 if tor["isPenalty"] else 0,
                1 if tor.get("isOvertime", False) else 0
            )

            # 4) SpielerSpieltInMannschaft speichern
            # team1 bedeutet Heimteam      

            if "team1" in tor:
            # normales Verhalten
                if tor["team1"]:
                    team_id = spiel["team1"]["teamId"]
                else:
                    team_id = spiel["team2"]["teamId"]
            else:
            # Fallback: wenn Eigentor -> gegnerisches Team
                if tor["isOwnGoal"]:
                # Eigentor -> Gegner bekommt das Tor
                    if tor.get("team1", None) is False:   # eigentlich Gastteam
                        team_id = spiel["team1"]["teamId"]
                    else:
                        team_id = spiel["team2"]["teamId"]
                else:
                    # team_id = spiel["team1"]["teamId"]
                    continue

            insert_spieler_spielt_in_mannschaft(
                spieler_id,
                team_id,
                saison
            )
