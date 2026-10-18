/****** Object:  View [dbo].[v_available_workingminutes_per_unit]    Script Date: 21.01.2023 23:51:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[v_available_workingminutes_per_unit] AS 
WITH niesprawne_urzadzenie AS 
(SELECT DISTINCT urzadzenie_id
FROM zadanie.dbo.[usterka] a
INNER JOIN zadanie.dbo.usterka_status b
ON a.status_id=b.id
WHERE b.opis in ('przekazanie informacji do centrali','diagnoza przyczyny awarii','rozpoczęcie naprawy','testy','przywrócenie do etapu działania produkcyjnego','urządzenia nie udaje się naprawić podlega kasacji')
), urzadzenia_per_oddzial AS (
SELECT odd.id as id_oddzial
      ,a.id as id_urzadzenia
	  ,CASE WHEN b.urzadzenie_id is not null THEN 0 ELSE 1 END as urzadzenie_sprawne
	  ,36*60 as dostepne_minuty_dla_urzadzenia
FROM zadanie.dbo.oddzial odd
LEFT JOIN zadanie.dbo.urzadzenie a
ON odd.id=a.oddzial_id
LEFT JOIN niesprawne_urzadzenie b
ON a.id=b.urzadzenie_id
), min_oddzial AS (
SELECT id_oddzial,sum(dostepne_minuty_dla_urzadzenia) as minuty_przerobowe_dla_oddzialu
FROM urzadzenia_per_oddzial
WHERE urzadzenie_sprawne=1
group by id_oddzial
)
SELECT a.id_oddzial
      ,a.minuty_przerobowe_dla_oddzialu
	  ,b.czas_drukowania_elementow_do_realizacji_in_min AS minuty_biezacych_realizowanych_zamowien
	  ,a.minuty_przerobowe_dla_oddzialu - b.czas_drukowania_elementow_do_realizacji_in_min as dostepne_roboczominuty
FROM min_oddzial a
LEFT JOIN zadanie.dbo.v_elementy_do_realizacji_aggr b
ON a.id_oddzial = b.oddzial_id
GO