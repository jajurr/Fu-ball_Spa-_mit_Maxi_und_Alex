# Sammlunng aller SQL Queries

Q_DB_HEALTHCHECK = "SELECT 1 AS ok;"

# Tore pro Spieltag für eine Liga + Saison
# MannschaftSpieltSpiel + Heimteim um eine Zuordnung zur Liga zu haben
Q_GOALS_PER_MATCHDAY = """
SELECT
    s.Spieltag,
    COUNT(*) AS Tore
FROM Tor t
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND s.Saison = ?
GROUP BY s.Spieltag
ORDER BY s.Spieltag;
"""
# Holt Kennzahlen (Spiele, Tore, Eigentore) für eine Liga + Saison
Q_KPIS = """
SELECT
    (SELECT COUNT(*)
     FROM Spiel s
     JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
     JOIN MannschaftSpieltInLiga msl
       ON msl.Saison = s.Saison
      AND msl.TeamID = mss.Heimannschaft
     WHERE msl.LigaName = ?
       AND s.Saison = ?) AS Spiele,

    (SELECT COUNT(*)
     FROM Tor t
     JOIN Spiel s ON s.MatchID = t.MatchID
     JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
     JOIN MannschaftSpieltInLiga msl
       ON msl.Saison = s.Saison
      AND msl.TeamID = mss.Heimannschaft
     WHERE msl.LigaName = ?
       AND s.Saison = ?) AS Tore,

    (SELECT COUNT(*)
     FROM SpielerSchiesstTor sst
     JOIN Tor t ON t.GoalID = sst.GoalID
     JOIN Spiel s ON s.MatchID = t.MatchID
     JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
     JOIN MannschaftSpieltInLiga msl
       ON msl.Saison = s.Saison
      AND msl.TeamID = mss.Heimannschaft
     WHERE msl.LigaName = ?
       AND s.Saison = ?
       AND sst.isOwnGoal = 1) AS Eigentore;
"""

# Alle Teams einer Liga in einer Saison
Q_TEAMS_IN_LEAGUE_SEASON = """
SELECT m.TeamID, m.Name, m.TeamLogo
FROM MannschaftSpieltInLiga msl
JOIN Mannschaft m ON m.TeamID = msl.TeamID
WHERE msl.LigaName = ?
  AND msl.Saison = ?
ORDER BY m.Name;
"""

# Alle Spiele eines Teams in einer Saison (mit Endergebnis)
Q_MATCHES_OF_TEAM_SEASON = """
WITH Endergebnis AS (
    SELECT e.MatchID,
           e.GoalsHeimmannschaft AS HeimTore,
           e.GoalsGastmannschaft AS GastTore
    FROM Ergebnis e
    JOIN (
        SELECT MatchID, MAX(ErgebnisID) AS MaxErgebnisID
        FROM Ergebnis
        WHERE isHalbzeitErgebnis = 0
        GROUP BY MatchID
    ) x ON x.MatchID = e.MatchID AND x.MaxErgebnisID = e.ErgebnisID
)
SELECT
    s.Saison,
    s.Spieltag,
    s.MatchID,
    mh.Name AS Heimmannschaft,
    mh.TeamLogo AS HeimLogo,
    mg.Name AS Gastmannschaft,
    mg.TeamLogo As GastLogo,
    ee.HeimTore,
    ee.GastTore
FROM Spiel s
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN Mannschaft mh ON mh.TeamID = mss.Heimannschaft
JOIN Mannschaft mg ON mg.TeamID = mss.Gastmannschaft
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
LEFT JOIN Endergebnis ee ON ee.MatchID = s.MatchID
WHERE msl.LigaName = ?
  AND s.Saison = ?
  AND (mss.Heimannschaft = ? OR mss.Gastmannschaft = ?)
ORDER BY CAST(s.Spieltag AS INTEGER), s.MatchID;
"""

# Match-Header: Saison, Spieltag, Teams, Datum, Ort
Q_MATCH_HEADER = """
SELECT
    s.MatchID,
    s.Saison,
    s.Spieltag,
    s.MatchDateTime,
    s.Ort,
    mh.Name AS Heimmannschaft,
    mh.TeamLogo AS HeimLogo,
    mg.Name AS Gastmannschaft,
    mg.TeamLogo AS GastLogo
FROM Spiel s
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN Mannschaft mh ON mh.TeamID = mss.Heimannschaft
JOIN Mannschaft mg ON mg.TeamID = mss.Gastmannschaft
WHERE s.MatchID = ?;
"""

# Endergebnis (isHalbzeitErgebnis=0)
Q_MATCH_ENDRESULT = """
SELECT
    e.GoalsHeimmannschaft AS HeimTore,
    e.GoalsGastmannschaft AS GastTore
FROM Ergebnis e
WHERE e.MatchID = ?
  AND e.isHalbzeitErgebnis = 0
ORDER BY e.ErgebnisID DESC
LIMIT 1;
"""

# Halbzeitergebnis (isHalbzeitErgebnis=1)
Q_MATCH_HALFTIME = """
SELECT
    e.GoalsHeimmannschaft AS HeimTore,
    e.GoalsGastmannschaft AS GastTore
FROM Ergebnis e
WHERE e.MatchID = ?
  AND e.isHalbzeitErgebnis = 1
ORDER BY e.ErgebnisID DESC
LIMIT 1;
"""

# Torliste für ein Match
Q_MATCH_GOALS = """
WITH MatchInfo AS (
  SELECT
    s.MatchID,
    s.Saison,
    mss.Heimannschaft AS HeimID,
    mss.Gastmannschaft AS GastID
  FROM Spiel s
  JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
  WHERE s.MatchID = ?
)
SELECT
    COALESCE(t.Spielminute, 999) AS Spielminute,
    p.Name AS Spieler,
    sst.isOwnGoal,
    sst.isPenalty,
    sst.isOvertime,
    t.GoalID,

    -- Teamzuordnung über SpielerSpieltInMannschaft in dieser Saison:
    CASE
      WHEN ssm.TeamID = mi.HeimID THEN 'Heim'
      WHEN ssm.TeamID = mi.GastID THEN 'Gast'
      ELSE 'Unbekannt'
    END AS Seite,

    mt.Name AS Mannschaft

FROM Tor t
JOIN SpielerSchiesstTor sst ON sst.GoalID = t.GoalID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN MatchInfo mi ON mi.MatchID = t.MatchID

LEFT JOIN SpielerSpieltInMannschaft ssm
  ON ssm.Saison = mi.Saison
 AND ssm.SpielerID = p.SpielerID
 AND ssm.TeamID IN (mi.HeimID, mi.GastID)

LEFT JOIN Mannschaft mt ON mt.TeamID = ssm.TeamID

WHERE t.MatchID = ?
ORDER BY COALESCE(t.Spielminute, 999), t.GoalID;
"""
# Top Scorer für eine Liga + Saison
Q_TOP_SCORER_SEASON = """
SELECT
    p.Name AS Spieler,
    COUNT(*) AS Tore
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND s.Saison = ?
  AND sst.isOwnGoal = 0
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
GROUP BY p.SpielerID
ORDER BY Tore DESC
LIMIT ?;
"""

# Top Scorer über alle Saisons für eine Liga
Q_TOP_SCORER_ALLTIME = """
SELECT
    p.Name AS Spieler,
    COUNT(*) AS Tore
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND sst.isOwnGoal = 0
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
GROUP BY p.SpielerID
ORDER BY Tore DESC
LIMIT ?;
"""

# Eigentore für Liga + Saison
Q_OWN_GOALS_SEASON = """
SELECT
    p.Name AS Spieler,
    s.Saison,
    s.Spieltag,
    t.Spielminute,
    mh.Name AS Heimteam,
    mg.Name AS Gastteam,
    s.MatchID
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN Mannschaft mh ON mh.TeamID = mss.Heimannschaft
JOIN Mannschaft mg ON mg.TeamID = mss.Gastmannschaft
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND s.Saison = ?
  AND sst.isOwnGoal = 1
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
ORDER BY CAST(s.Spieltag AS INTEGER), s.MatchID, COALESCE(t.Spielminute, 999), t.GoalID;
"""

# Eigentore für Liga über alle Saisons
Q_OWN_GOALS_ALLTIME = """
SELECT
    p.Name AS Spieler,
    s.Saison,
    s.Spieltag,
    t.Spielminute,
    mh.Name AS Heimteam,
    mg.Name AS Gastteam,
    s.MatchID
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN Mannschaft mh ON mh.TeamID = mss.Heimannschaft
JOIN Mannschaft mg ON mg.TeamID = mss.Gastmannschaft
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND sst.isOwnGoal = 1
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
ORDER BY s.Saison, CAST(s.Spieltag AS INTEGER), s.MatchID, COALESCE(t.Spielminute, 999), t.GoalID;
"""

# Top Eigentorschützen einer Liga + Saison
Q_TOP_OWN_GOAL_SCORERS_SEASON = """
SELECT
    p.Name AS Spieler,
    COUNT(*) AS Eigentore
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND s.Saison = ?
  AND sst.isOwnGoal = 1
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
GROUP BY p.SpielerID
ORDER BY Eigentore DESC, Spieler ASC
LIMIT ?;
"""

# Top Eigentorschützen einer Liga über alle Saisons
Q_TOP_OWN_GOAL_SCORERS_ALLTIME = """
SELECT
    p.Name AS Spieler,
    COUNT(*) AS Eigentore
FROM SpielerSchiesstTor sst
JOIN Tor t ON t.GoalID = sst.GoalID
JOIN Spiel s ON s.MatchID = t.MatchID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
JOIN MannschaftSpieltInLiga msl
  ON msl.Saison = s.Saison
 AND msl.TeamID = mss.Heimannschaft
WHERE msl.LigaName = ?
  AND sst.isOwnGoal = 1
  AND p.Name IS NOT NULL
  AND TRIM(p.Name) NOT IN ('', '0')
GROUP BY p.SpielerID
ORDER BY Eigentore DESC, Spieler ASC
LIMIT ?;
"""

# Tabelle/Standings aus der DB (Liga + Saison)
# Nutzt Endergebnis (isHalbzeitErgebnis=0)
Q_TABLE_STANDINGS = """
WITH Endstand AS (
  SELECT
    e.MatchID,
    e.GoalsHeimmannschaft AS HeimTore,
    e.GoalsGastmannschaft AS GastTore
  FROM Ergebnis e
  WHERE e.isHalbzeitErgebnis = 0
),
Games AS (
  -- Heimteam
  SELECT
    s.Saison,
    mss.Heimannschaft AS TeamID,
    Endstand.HeimTore AS Tore,
    Endstand.GastTore AS Gegentore,
    CASE
      WHEN Endstand.HeimTore > Endstand.GastTore THEN 3
      WHEN Endstand.HeimTore = Endstand.GastTore THEN 1
      ELSE 0
    END AS Punkte,
    CASE WHEN Endstand.HeimTore > Endstand.GastTore THEN 1 ELSE 0 END AS Siege,
    CASE WHEN Endstand.HeimTore = Endstand.GastTore THEN 1 ELSE 0 END AS Unentschieden,
    CASE WHEN Endstand.HeimTore < Endstand.GastTore THEN 1 ELSE 0 END AS Niederlagen,
    1 AS Spiele
  FROM Spiel s
  JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
  JOIN Endstand ON Endstand.MatchID = s.MatchID
  JOIN MannschaftSpieltInLiga msl
    ON msl.Saison = s.Saison AND msl.TeamID = mss.Heimannschaft
  WHERE msl.LigaName = ?
    AND s.Saison = ?

  UNION ALL

  -- Gastteam
  SELECT
    s.Saison,
    mss.Gastmannschaft AS TeamID,
    Endstand.GastTore AS Tore,
    Endstand.HeimTore AS Gegentore,
    CASE
      WHEN Endstand.GastTore > Endstand.HeimTore THEN 3
      WHEN Endstand.GastTore = Endstand.HeimTore THEN 1
      ELSE 0
    END AS Punkte,
    CASE WHEN Endstand.GastTore > Endstand.HeimTore THEN 1 ELSE 0 END AS Siege,
    CASE WHEN Endstand.GastTore = Endstand.HeimTore THEN 1 ELSE 0 END AS Unentschieden,
    CASE WHEN Endstand.GastTore < Endstand.HeimTore THEN 1 ELSE 0 END AS Niederlagen,
    1 AS Spiele
  FROM Spiel s
  JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
  JOIN Endstand ON Endstand.MatchID = s.MatchID
  JOIN MannschaftSpieltInLiga msl
    ON msl.Saison = s.Saison AND msl.TeamID = mss.Heimannschaft
  WHERE msl.LigaName = ?
    AND s.Saison = ?
)
SELECT
  m.Name AS Team,
  SUM(Spiele) AS Spiele,
  SUM(Siege) AS Siege,
  SUM(Unentschieden) AS Unentschieden,
  SUM(Niederlagen) AS Niederlagen,
  SUM(Tore) AS Tore,
  SUM(Gegentore) AS Gegentore,
  (SUM(Tore) - SUM(Gegentore)) AS Tordifferenz,
  SUM(Punkte) AS Punkte
FROM Games g
JOIN Mannschaft m ON m.TeamID = g.TeamID
GROUP BY g.TeamID
ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC, Team ASC;
"""


# Meister pro Saison + Liga
Q_CHAMPIONS_BY_SEASON = """
WITH Endstand AS (
  SELECT
    e.MatchID,
    e.GoalsHeimmannschaft AS HeimTore,
    e.GoalsGastmannschaft AS GastTore
  FROM Ergebnis e
  WHERE e.isHalbzeitErgebnis = 0
),
Games AS (
  -- Heimteam
  SELECT
    s.Saison,
    mss.Heimannschaft AS TeamID,
    Endstand.HeimTore AS Tore,
    Endstand.GastTore AS Gegentore,
    CASE
      WHEN Endstand.HeimTore > Endstand.GastTore THEN 3
      WHEN Endstand.HeimTore = Endstand.GastTore THEN 1
      ELSE 0
    END AS Punkte,
    1 AS Spiele
  FROM Spiel s
  JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
  JOIN Endstand ON Endstand.MatchID = s.MatchID
  JOIN MannschaftSpieltInLiga msl
    ON msl.Saison = s.Saison AND msl.TeamID = mss.Heimannschaft
  WHERE msl.LigaName = ?
  
  UNION ALL
  
  -- Gastteam
  SELECT
    s.Saison,
    mss.Gastmannschaft AS TeamID,
    Endstand.GastTore AS Tore,
    Endstand.HeimTore AS Gegentore,
    CASE
      WHEN Endstand.GastTore > Endstand.HeimTore THEN 3
      WHEN Endstand.GastTore = Endstand.HeimTore THEN 1
      ELSE 0
    END AS Punkte,
    1 AS Spiele
  FROM Spiel s
  JOIN MannschaftSpieltSpiel mss ON mss.MatchID = s.MatchID
  JOIN Endstand ON Endstand.MatchID = s.MatchID
  JOIN MannschaftSpieltInLiga msl
    ON msl.Saison = s.Saison AND msl.TeamID = mss.Heimannschaft
  WHERE msl.LigaName = ?
),
TableAgg AS (
  SELECT
    Saison,
    TeamID,
    SUM(Punkte) AS Punkte,
    SUM(Tore) AS Tore,
    SUM(Gegentore) AS Gegentore,
    (SUM(Tore) - SUM(Tore)) AS Tordifferenz,
    SUM(Spiele) AS Spiele
  FROM Games
  GROUP BY Saison, TeamID
),
-- Nur Saisons behalten, wo alle Teams 34 Spiele haben (robust!)
CompletedSeasons AS (
  SELECT Saison
  FROM TableAgg
  GROUP BY Saison
  HAVING MIN(Spiele) = 34 AND MAX(Spiele) = 34
),
Ranked AS (
  SELECT
    t.Saison,
    t.TeamID,
    t.Punkte,
    t.Tordifferenz,
    t.Tore,
    ROW_NUMBER() OVER (
      PARTITION BY t.Saison
      ORDER BY t.Punkte DESC, t.Tordifferenz DESC, t.Tore DESC, t.TeamID ASC
    ) AS Platz
  FROM TableAgg t
  JOIN CompletedSeasons c ON c.Saison = t.Saison
)
SELECT
  r.Saison,
  m.Name AS Meister,
  r.Punkte,
  r.Tordifferenz,
  r.Tore
FROM Ranked r
JOIN Mannschaft m ON m.TeamID = r.TeamID
WHERE r.Platz = 1
ORDER BY r.Saison;
"""