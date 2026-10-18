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



/****** Object:  StoredProcedure [dbo].[SumOfAllInactiveMinutes]    Script Date: 17.01.2023 23:30:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
ALTER procedure [dbo].[SumOfAllInactiveMinutes] 
(
	-- Add the parameters for the function here
	@date_from datetime,
	@date_to datetime
)
AS
BEGIN
	
DECLARE @overal_sum int = 0
DECLARE @individual_sum int = 0
--DECLARE @date_from datetime = '2022-12-07'
--DECLARE @date_to datetime = '2022-12-16'

DECLARE kursor CURSOR FOR SELECT DISTINCT urzadzenie_id from zadanie.dbo.usterka
DECLARE @id int
OPEN kursor 
FETCH NEXT FROM kursor into @id
WHILE @@FETCH_STATUS = 0
BEGIN

--SELECT @id, @date_from, @date_to
--exec zadanie.dbo.SumOfInactiveMinutes @date_from, @date_to, @id

exec @individual_sum = zadanie.dbo.SumOfInactiveMinutes2 @data1=@date_from, @data2=@date_to, @deviceid=@id

--SELECT @individual_sum

SET @Overal_sum = @Overal_sum + ISNULL(@individual_sum, 0)
--SELECT @overal_sum

FETCH NEXT FROM kursor INTO @id

END
CLOSE kursor
DEALLOCATE kursor

SELECT @overal_sum

END

GO


/****** Object:  StoredProcedure [dbo].[Unit_with_longest_malfunctions]    Script Date: 17.01.2023 23:30:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE procedure [dbo].[Unit_with_longest_malfunctions] 
(
	-- Add the parameters for the function here
	@date_from datetime,
	@date_to datetime
)
AS
BEGIN
	
DECLARE @individual_sum int = 0

declare @tmp_table table (id int, malfunciton_time int)

DECLARE kursor CURSOR FOR SELECT DISTINCT urzadzenie_id from zadanie.dbo.usterka
DECLARE @id int
OPEN kursor 
FETCH NEXT FROM kursor into @id
WHILE @@FETCH_STATUS = 0
BEGIN

--SELECT @id, @date_from, @date_to
--exec zadanie.dbo.SumOfInactiveMinutes @date_from, @date_to, @id

exec @individual_sum = zadanie.dbo.SumOfInactiveMinutes2 @data1=@date_from, @data2=@date_to, @deviceid=@id

--SELECT @individual_sum

INSERT INTO @tmp_table values (@id, ISNULL(@individual_sum, 0))
--SELECT @overal_sum

FETCH NEXT FROM kursor INTO @id

END
CLOSE kursor
DEALLOCATE kursor

SELECT b.oddzial_id,sum(a.malfunciton_time) as malfunction_time_sum
into #temp
FROM @tmp_table a
INNER JOIN zadanie.dbo.urzadzenie b
ON a.id = b.id
GROUP BY b.oddzial_id
ORDER BY 2 DESC

SELECT TOP 1 oddzial_id
From #temp



END

GO
