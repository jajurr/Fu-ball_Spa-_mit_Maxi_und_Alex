# api/openliga.py
import urllib.request
import json

BASE_URL = "https://api.openligadb.de"

def fetch(endpoint: str):
    """Generic fetch function."""
    url = BASE_URL + endpoint
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode())

def get_bundesliga_matches(season=None):
    """Fetch all match data for first Bundesliga."""
    if season:
        return fetch(f"/getmatchdata/bl1/{season}")
    return fetch("/getmatchdata/bl1")

def get_bundesliga_teams(season):
    """
    Alle Teams einer Bundesliga-Saison abrufen.
    Gibt leere Liste zurück, wenn die Saison nicht existiert.
    """
    try:
        return fetch(f"/getavailableteams/bl1/{season}")
    except:
        return []  # Saison existiert nicht

def get_historische_saisons(start_year=2001):
    """
    Prüft ab Startjahr bis zur aktuellen Saison,
    welche Saisons tatsächlich Daten liefern
    """
    from datetime import datetime
    current_year = datetime.now().year
    vorhandene_saisons = []

    for year in range(start_year, current_year + 1):
        teams = get_bundesliga_teams(year)
        if teams:  # Wenn die API Teams liefert
            vorhandene_saisons.append(year)

    return vorhandene_saisons

def get_spiele_einer_saison(liga, saison):
    """Gibt alle Spiele einer bestimmten Saison zurück."""
    try:
        return fetch(f"/getmatchdata/{liga}/{saison}")
    except:
        return []  # Spiele der Saison existieren nicht
    
def get_goalgetters(liga, saison):
    try:
        return fetch(f"/getgoalgetters/{liga}/{saison}")
    except:
        return []  # Golatgetter existieren nicht
    
def get_einzelspiel(matchID):
    try:
        return fetch(f"/getmatchdata/{matchID}")
    except:
        return []  # Einzelspiel existieren nicht