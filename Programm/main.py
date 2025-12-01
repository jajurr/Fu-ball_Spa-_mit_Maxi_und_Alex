from db.database import test_conenction
from api.openliga import get_bundesliga_matches
from logic.converter import import_teams_historisch, import_mannschaft_spielt_in_liga, import_spiele_saison
from datetime import datetime
def main():
    test_conenction()
    print("Verbindung getestet.")

    #print("Importiere alle historischen Teams ab 2001 ...")
    #import_teams_historisch()
    #print("Teams importiert.")

    # Mannschaft-Liga-Zuordnungen importieren
    #print("Importiere MannschaftSpieltInLiga für alle Saisons ab 2001 ...")
    #import_mannschaft_spielt_in_liga()
    #print("Fertig!")

    import_spiele_saison("bl1", 2001)
    # Importiere alle Saisons ab 2002 bis heute

    
if __name__ == "__main__":
    main()