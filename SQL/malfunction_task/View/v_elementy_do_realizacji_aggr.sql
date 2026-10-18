/****** Object:  View [dbo].[v_elementy_do_realizacji_aggr]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [dbo].[v_elementy_do_realizacji_aggr] AS 
SELECT a.oddzial_id,count(id_zlecenie_element) liczba_Elementow_do_realizacji,sum(typ_time_min) czas_drukowania_elementow_do_realizacji_in_min
FROM zadanie.dbo.zlecenia a
INNER JOIN zadanie.dbo.zlecenie_element b
ON id_zlecenia=b.id_zlecenie
INNER JOIN zadanie.dbo.zlecenie_element_status c
ON b.id_status=c.id_zlecenie_status
INNER JOIN element_typ d
ON b.id_type = d.id_typ
WHERE c.zlecenie_Status in ('To Do')
group by a.oddzial_id
GO