# api/openliga.py
import urllib.request
import json

#URL für openligaDB
BASE_URL = "https://api.openligadb.de"

def fetch(endpoint: str):
    """
    Generische Fetch
    """
    url = BASE_URL + endpoint
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode())

def get_liga_matches(league ,season=None):
    """Fetch all match data for first Bundesliga."""
    if season:
        return fetch(f"/getmatchdata/{league}]/{season}")
    return fetch("/getmatchdata/{league}")

def get_bundesliga_teams(league,season):
    """
    Alle Teams einer Sasion - leer wenn es keine Saison gibt
    """
    try:
        return fetch(f"/getavailableteams/{league}/{season}")
    except:
        return []  # Saison existiert nicht

def get_historische_saisons(league,start_year=2001):
    """
    Holt alle Saisons ab 2001
    """
    from datetime import datetime
    current_year = datetime.now().year
    vorhandene_saisons = []

    for year in range(start_year, current_year + 1):
        teams = get_bundesliga_teams(league,year)
        if teams:  # Wenn die API Teams liefert
            vorhandene_saisons.append(year)

    return vorhandene_saisons

def get_spiele_einer_saison(liga, saison):
    """
    Gibt alle Spiele für eine Liga/Saison
    """
    try:
        return fetch(f"/getmatchdata/{liga}/{saison}")
    except:
        return []  # Spiele der Saison existieren nicht
    
def get_goalgetters(liga, saison):
    """
    Gibt alle Toschützen für eine Liga/Saison
    """
    try:
        return fetch(f"/getgoalgetters/{liga}/{saison}")
    except:
        return []  # Golatgetter existieren nicht
    
def get_einzelspiel(matchID):
    """
    Gibt die Daten eines einzelnes Spieles per MatchID zurück
    """
    try:
        return fetch(f"/getmatchdata/{matchID}")
    except:
        return []  # Einzelspiel existieren nicht