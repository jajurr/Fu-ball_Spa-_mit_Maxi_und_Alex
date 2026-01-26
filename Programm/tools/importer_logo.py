import sqlite3
from pathlib import Path

DB_PATH = "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Fussball.db"
#"C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\"
# TeamID -> Dateipfad
LOGOS = {
    #199: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Heidenheim.png",
    #65: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Koeln_Logo_2014–.svg.png",
    #80: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Union_Berlin_Logo.svg.png",
    #81: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Mainz_05.svg.png",    
    #6: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Bayer_Leverkusen_Logo.svg.png",   
    #7: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Borussia_Dortmund_logo.svg.png",   
    #87: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Borussia_Mönchengladbach_logo.svg.png",   
    #91: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Eintracht_Frankfurt_1998.svg.png",   
    #95: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_FC_Augsburg.svg.png",   
    #40: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FC_Bayern_München_logo_(2024).svg.png",   
    #98: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Pauli.png",   
    #100: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Hamburger_SV_logo.svg.png",   
    #1635: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\2019-07-12_Fußball;_Freundschaftsspiel_RB_Leipzig_-_FC_Zürich_1DX_0881_by_Stepro_2.png",   
    #112: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SC_Freiburg_Logo.svg.png",   
    #134: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV-Werder-Bremen-Logo.svg.png",   
    #175: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_TSG_Hoffenheim.svg.png",   
    #16: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\VfB_Stuttgart_1893_Logo.svg.png",   
    #131: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo-VfL-Wolfsburg.svg.png",   
    76: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_1_FC_Kaiserslautern.svg.png",   
    78: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Magdeburg.svg.png",   
    79: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Nürnberg_logo.svg.png", 
    83: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Arminia_Bielefeld_Logo_2021–.svg.png", 
    177: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_SG_Dynamo_Dresden_neu.svg.png", 
    74: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Eintracht_Braunschweig.svg.png", 
    9: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FC_Schalke_04_Logo.svg.png", 
    185: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Fortuna_Düsseldorf.svg.png", 
    55: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Hannover_96_Logo.svg.png", 
    54: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Hertha_BSC_Logo_2012.svg.png", 
    104: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Holstein_Kiel_Logo.svg.png", 
    105: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Karlsruher_SC_Logo_2.svg.png", 
    188: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SC_Preussen_Muenster_Logo_2018.svg.png", 
    31: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SC_Paderborn_07_Logo_new.svg.png", 
    198: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Elversberg_Logo_2021.svg.png", 
    118: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Darmstadt_98_Logo.svg.png", 
    115: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SpVgg_Greuther_Fürth_2017.svg.png", 
    129: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\VfL_Bochum_logo.svg.png", 
}

def update_team_logo(team_id: int, logo_path: str):
    path = Path(logo_path)
    if not path.exists():
        print(f"Datei nicht gefunden: {logo_path}")
        return

    logo_bytes = path.read_bytes()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute(
            "UPDATE Mannschaft SET TeamLogo = ? WHERE TeamID = ?",
            (logo_bytes, team_id)
        )
        conn.commit()

    print(f"Logo gespeichert: TeamID={team_id} ({logo_path})")

def main():
    for team_id, path in LOGOS.items():
        update_team_logo(team_id, path)

if __name__ == "__main__":
    main()