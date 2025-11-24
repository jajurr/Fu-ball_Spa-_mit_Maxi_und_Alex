from api.openliga import get_bundesliga_teams, get_historische_saisons
from db.database import insert_team, insert_mannschaft_spielt_in_liga

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