from api.openliga import get_bundesliga_teams, get_historische_saisons, get_spiele_einer_saison, get_goalgetters, get_einzelspiel
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

        goals = spiel.get("goals", [])

        if not goals:
            continue

        einzelspiel = get_einzelspiel(match_id)

        goals = einzelspiel.get("goals", [])

        #Sortierung der Liste nach Spielminuten
        goals = sorted(goals, key=lambda g: ((g.get("matchMinute") or 999), g["goalID"]))


        prev_score1 = 0
        prev_score2 = 0
        
        for tor in goals:

            goal_id = tor["goalID"]
            minute = tor.get("matchMinute")
            spieler_id = tor["goalGetterID"]
            spieler_name = tor.get("goalGetterName")

            # Spieler ohne Namen ignorieren (API-Fehler vermeiden)
            if not spieler_name or spieler_name.strip() in ("", "0"):
                continue

            score1 = tor.get("scoreTeam1")
            score2 = tor.get("scoreTeam2")

            is_own = tor.get("isOwnGoal", False)

            team_id = None

            # --- Normales Tor Team 1 ---
            if score1 == prev_score1 + 1 and score2 == prev_score2 and not is_own:
                team_id = spiel["team1"]["teamId"]

            # --- Normales Tor Team 2 ---
            elif score2 == prev_score2 + 1 and score1 == prev_score1 and not is_own:
                team_id = spiel["team2"]["teamId"]

            # --- Eigentor von Team 1 (Team 2 bekommt Tor) ---
            elif score2 == prev_score2 + 1 and score1 == prev_score1 and is_own:
                team_id = spiel["team1"]["teamId"]

            # --- Eigentor von Team 2 (Team 1 bekommt Tor) ---
            elif score1 == prev_score1 + 1 and score2 == prev_score2 and is_own:
                team_id = spiel["team2"]["teamId"]

            # 6. Fallback: unplausibel → überspringen
            else:
                prev_score1 = score1
                prev_score2 = score2
                continue

            # Datenbanken füllen
            insert_spieler(spieler_id, spieler_name)
            insert_tor(goal_id, minute, match_id)
            insert_spieler_schiesst_tor(
                spieler_id,
                goal_id,
                1 if tor.get("isOwnGoal", False) else 0,
                1 if tor.get("isPenalty", False) else 0,
                1 if tor.get("isOvertime", False) else 0
            )
            insert_spieler_spielt_in_mannschaft(
                spieler_id,
                team_id,
                saison
            )

            # 7. Score nach dem Tor setzen
            prev_score1 = score1
            prev_score2 = score2