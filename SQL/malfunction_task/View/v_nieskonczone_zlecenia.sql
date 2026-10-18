/****** Object:  View [dbo].[v_nieskonczone_zlecenia]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [dbo].[v_nieskonczone_zlecenia] AS 
SELECT a.oddzial_id, count(DISTINCT numer_zlecenia) as nieskonczone_zlecenia
FROM zadanie.dbo.zlecenia a
INNER JOIN zadanie.dbo.zlecenie_element b
ON id_zlecenia=b.id_zlecenie
INNER JOIN zadanie.dbo.zlecenie_element_status c
ON b.id_status=c.id_zlecenie_status
WHERE c.zlecenie_Status in ('To Do','In Progress')
group by a.oddzial_id
GO