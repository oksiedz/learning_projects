/****** Object:  StoredProcedure [dbo].[Unit_with_longest_malfunctions]    Script Date: 18.01.2023 22:36:29 ******/
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

exec @individual_sum = zadanie.dbo.SumOfInactiveMinutes @data1=@date_from, @data2=@date_to, @deviceid=@id, @ifreturn = 1

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