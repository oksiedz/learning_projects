/****** Object:  View [dbo].[statuses_fraction]    Script Date: 17.01.2023 23:30:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [dbo].[statuses_fraction] as
SELECT x.status
      ,CONVERT(float, count_case) / CONVERT(float, all_rows) AS fraction
FROM (
      SELECT a.status
            ,count(1) as count_case
            ,b.all_rows
      FROM zadanie.dbo.urzadzenie a
      LEFT JOIN (
                 SELECT count(1) as all_rows
                 From zadanie.dbo.urzadzenie
                ) b
      ON 1 = 1
      group by a.status,b.all_rows
     ) x
GO