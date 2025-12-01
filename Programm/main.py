from db.database import test_conenction
from api.openliga import get_bundesliga_matches, get_spiele_einer_saison
from logic.converter import import_teams_historisch, import_mannschaft_spielt_in_liga, import_spiele_saison, import_goalgetters_saison
from datetime import datetime
def main():
    test_conenction()
    print("Verbindung getestet.")

    #print("Importiere alle historischen Teams ab 2001 ...")
    #import_teams_historisch()
    #print("Teams importiert.")

    #Mannschaft-Liga-Zuordnungen importieren
    #print("Importiere MannschaftSpieltInLiga für alle Saisons ab 2001 ...")
    #import_mannschaft_spielt_in_liga(  )
    #print("Fertig!")

    aktuelles_jahr = datetime.now().year

    print(f"Importiere Spiele der Bundesliga von 2001 bis {aktuelles_jahr}...")

    for saison in range(2001, aktuelles_jahr + 1):
        import_spiele_saison("bl1", saison)
        import_goalgetters_saison("bl1", saison)
    print("Fertig!")
    #spiele = get_spiele_einer_saison("bl1", 2010)
    #print(spiele[0]["goals"])

if __name__ == "__main__":
    main()