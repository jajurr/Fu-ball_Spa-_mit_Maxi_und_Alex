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
    #76: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_1_FC_Kaiserslautern.svg.png",   
    #78: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Magdeburg.svg.png",   
    #79: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\1._FC_Nürnberg_logo.svg.png", 
    #83: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Arminia_Bielefeld_Logo_2021–.svg.png", 
    #177: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_SG_Dynamo_Dresden_neu.svg.png", 
    #74: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Eintracht_Braunschweig.svg.png", 
    #9: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FC_Schalke_04_Logo.svg.png", 
    #185: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Fortuna_Düsseldorf.svg.png", 
    #55: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Hannover_96_Logo.svg.png", 
    #54: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Hertha_BSC_Logo_2012.svg.png", 
    #104: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Holstein_Kiel_Logo.svg.png", 
    #105: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Karlsruher_SC_Logo_2.svg.png", 
    #188: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SC_Preussen_Muenster_Logo_2018.svg.png", 
    #31: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SC_Paderborn_07_Logo_new.svg.png", 
    #198: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Elversberg_Logo_2021.svg.png", 
    #118: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Darmstadt_98_Logo.svg.png", 
    #115: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SpVgg_Greuther_Fürth_2017.svg.png", 
    #129: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\VfL_Bochum_logo.svg.png", 
    23: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Alemannia_Aachen_2010.svg.png", 
    29: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Kickers_Offenbach.svg.png",
    36: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\VfL_Osnabrueck_Logo_2021–.svg.png",
    66: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Fc_erzgebirge_aue.svg.png",
    69: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_FC_Carl_Zeiss_Jena.svg.png",
    73: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Wacker_Burghausen.svg.png",
    93: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FC_Energie_Cottbus_Logo_1966.svg.png",
    102: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\F.C._Hansa_Rostock_Logo.svg.png",
    107: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Msv_duisburg_(2017).svg.png",
    109: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_Rot-Weiss_Essen.svg.png",
    110: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Rot_Weiss_Ahlen.svg.png",
    116: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SpVgg_Unterhaching_Logo_2012.svg.png",
    119: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Sandhausen.svg.png",
    123: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Logo_TSG_Hoffenheim.svg.png",
    125: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\TSV_1860_München.svg.png",
    127: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\TuS_Koblenz.svg.png",
    171: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FC-Ingolstadt_logo.svg.png",
    172: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\FSV_Frankfurt_1899.svg.png",
    173: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Rot_Weiss_Oberhausen_Logo.svg.png",
    174: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SV_Wehen_Logo.png",
    181: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Jahn_Regensburg_logo2014.svg.png",   
    183: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\VfR_Aalen_Wappen.svg.png",
    398: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\Würzburger_Kickers_Logo.svg.png",
    564: "C:\\Users\\Arjurr\\Desktop\\Uni\\IuK2\\Sqlite\\Logos\\SSV_Ulm_1846_Fussball.svg.png",          
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