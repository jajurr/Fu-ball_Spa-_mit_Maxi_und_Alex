import sqlite3

#Pfad zur Datenbank, ggf. tauschen
DB_PATH = "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Fussball.db"

def get_connection():
    #Stellt die Verbindung zur SQLite-Datenbank her
    return sqlite3.connect(DB_PATH)

def test_conenction():
    with get_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Mannschaft')
            rows = cur.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print("Fehler beim Einfügen:", e)

def insert_team(team):
    """
    team = (TeamID, Name)
    """
    with get_connection() as conn:
        try:
            conn.execute("""
                INSERT OR REPLACE INTO Mannschaft (TeamID, Name)
                VALUES (?, ?)
            """, team)
            conn.commit()
        except sqlite3.Error as e:
            print("Fehler beim Einfügen:", e)

def insert_mannschaft_spielt_in_liga(eintrag):
    """
    eintrag = (Saison, LigaName, TeamID)
    """
    with get_connection() as conn:
        try:
            conn.execute("""
                INSERT OR REPLACE INTO MannschaftSpieltInLiga (Saison, LigaName, TeamID)
                VALUES (?, ?, ?)
            """, eintrag)
            conn.commit()
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in MannschaftSpieltInLiga:", e)

def insert_spiel(match_id, date_time, ort):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO Spiel (MatchID, MatchDateTime, Ort)
                VALUES (?, ?, ?)
            """, (match_id, date_time, ort))
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in Spiel:", e)

def insert_mannschaft_spielt_spiel(match_id, heim, gast):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO MannschaftSpieltSpiel (MatchID, Heimannschaft, Gastmannschaft)
                VALUES (?, ?, ?)
            """, (match_id, heim, gast))
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in MannschaftSpieltSpiel:", e)

def insert_ergebnis(ergebnis_id, match_id, gast, heim, halbzeit):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO Ergebnis (ErgebnisID, MatchID, GoalsGastmannschaft, GoalsHeimmannschaft, isHalbzeitErgebnis)
                VALUES (?, ?, ?, ?, ?)
            """, (ergebnis_id, match_id, gast, heim, halbzeit))
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in Ergebnis:", e)        