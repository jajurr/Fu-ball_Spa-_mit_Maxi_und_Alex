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
    """eintrag = (Saison, LigaName, TeamID)"""
    with get_connection() as conn:
        try:
            conn.execute("""
                INSERT OR REPLACE INTO MannschaftSpieltInLiga (Saison, LigaName, TeamID)
                VALUES (?, ?, ?)
            """, eintrag)
            conn.commit()
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in MannschaftSpieltInLiga:", e)