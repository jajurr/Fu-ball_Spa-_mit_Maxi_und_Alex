# Hier sammeln wir nach und nach alle SQL-Abfragen zentral.
# Das macht die Views sauber und gut wartbar.

Q_DB_HEALTHCHECK = "SELECT 1 AS ok;"

Q_DB_HEALTHCHECK = "SELECT 1 AS ok;"

# Tore pro Spieltag für eine Liga + Saison
# Wir nutzen msl + Heimteam-Verknüpfung, um das Spiel eindeutig einer Liga zuzuordnen.
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

# Kleine Kennzahlen (Spiele, Tore, Eigentore) für Liga + Saison
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
SELECT m.TeamID, m.Name
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
    mh.Name AS Heimteam,
    mg.Name AS Gastteam,
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
    mh.Name AS Heimteam,
    mg.Name AS Gastteam
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

# Halbzeit (isHalbzeitErgebnis=1)
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

# Torliste (nur Tore, die einen Spieler haben)
Q_MATCH_GOALS = """
SELECT
    COALESCE(t.Spielminute, 999) AS Spielminute,
    p.Name AS Spieler,
    sst.isOwnGoal,
    sst.isPenalty,
    sst.isOvertime,
    t.GoalID
FROM Tor t
JOIN SpielerSchiesstTor sst ON sst.GoalID = t.GoalID
JOIN Spieler p ON p.SpielerID = sst.SpielerID
WHERE t.MatchID = ?
ORDER BY COALESCE(t.Spielminute, 999), t.GoalID;
"""

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

# Top Scorer über alle Saisons für eine Liga (ohne Eigentore)
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
# Nutzt Endergebnis (isHalbzeitErgebnis=0). Zählt nur Spiele, für die ein Endergebnis existiert.
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
    Endstand.HeimTore AS ToreFuer,
    Endstand.GastTore AS ToreGegen,
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
    Endstand.GastTore AS ToreFuer,
    Endstand.HeimTore AS ToreGegen,
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
  SUM(Siege) AS S,
  SUM(Unentschieden) AS U,
  SUM(Niederlagen) AS N,
  SUM(ToreFuer) AS ToreFuer,
  SUM(ToreGegen) AS ToreGegen,
  (SUM(ToreFuer) - SUM(ToreGegen)) AS Diff,
  SUM(Punkte) AS Punkte
FROM Games g
JOIN Mannschaft m ON m.TeamID = g.TeamID
GROUP BY g.TeamID
ORDER BY Punkte DESC, Diff DESC, ToreFuer DESC, Team ASC;
"""


# Meister pro Saison (für eine Liga) - aus DB berechnet
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
    Endstand.HeimTore AS ToreFuer,
    Endstand.GastTore AS ToreGegen,
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
    Endstand.GastTore AS ToreFuer,
    Endstand.HeimTore AS ToreGegen,
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
    SUM(ToreFuer) AS ToreFuer,
    SUM(ToreGegen) AS ToreGegen,
    (SUM(ToreFuer) - SUM(ToreGegen)) AS Diff,
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
    t.Diff,
    t.ToreFuer,
    ROW_NUMBER() OVER (
      PARTITION BY t.Saison
      ORDER BY t.Punkte DESC, t.Diff DESC, t.ToreFuer DESC, t.TeamID ASC
    ) AS Platz
  FROM TableAgg t
  JOIN CompletedSeasons c ON c.Saison = t.Saison
)
SELECT
  r.Saison,
  m.Name AS Meister,
  r.Punkte,
  r.Diff,
  r.ToreFuer
FROM Ranked r
JOIN Mannschaft m ON m.TeamID = r.TeamID
WHERE r.Platz = 1
ORDER BY r.Saison;
"""