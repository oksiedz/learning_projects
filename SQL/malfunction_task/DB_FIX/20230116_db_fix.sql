/****** Object:  UserDefinedFunction [dbo].[shift_no]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
ALTER FUNCTION [dbo].[shift_no]
(
	-- Add the parameters for the function here
	@datetime datetime
)
RETURNS int
AS
BEGIN
	
	DECLARE @shift_no int
	SET @shift_no = CASE WHEN datepart(hour, @datetime) < 6 THEN 3
	                     WHEN datepart(hour, @datetime) < 14 tHEN 1
						 WHEN datepart(hour, @datetime) > 22 tHEN 3
						 WHEN @datetime is null then null
						 ELSE 2
						 END

	RETURN @shift_no

END
GO


/****** Object:  UserDefinedFunction [dbo].[defects_per_unit]    Script Date: 16.01.2023 23:29:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[defects_per_unit]
(	
	@data1 datetime,
	@data2 datetime
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT TOP 1 urz.oddzial_id,count(ust.id) as count_no
FROM zadanie.dbo.usterka ust
INNER JOIN zadanie.dbo.urzadzenie urz
ON ust.urzadzenie_id=urz.id
WHERE ust.data_zgloszenia between @data1 and @data2
group by urz.oddzial_id

)

GO

/****** Object:  UserDefinedFunction [dbo].[unit_with_most_defects]    Script Date: 16.01.2023 23:29:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[unit_with_most_defects]
(	
	@data1 datetime,
	@data2 datetime
)
RETURNS int 
AS
BEGIN

DECLARE @temp TABLE (oddzial int, count_no int)

INSERT INTO @temp
SELECT * from zadanie.dbo.[defects_per_unit] (@data1,@data2)
DECLARE @oddzial_id int =
(SELECT TOP 1 oddzial
fROM @temp
ORDER BY count_no DESC)

RETURN @oddzial_id
END
GO

/****** Object:  StoredProcedure [dbo].[SumOfInactiveMinutes2]    Script Date: 16.01.2023 23:29:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE procedure [dbo].[SumOfInactiveMinutes2] 
(
	-- Add the parameters for the function here
	@data1 datetime,
	@data2 datetime,
	@deviceid int
)
AS
BEGIN
	
	declare
	@tmp_table_base table (id int, id_awaria int, poczatek_naprawy datetime, koniec_naprawy datetime)
	INSERT INTO @tmp_table_base
(
    id, id_awaria, poczatek_naprawy, koniec_naprawy)
EXEC zadanie.[dbo].[getAgregateIntervals] @data1, @data2, @deviceid

DECLARE @time int = 
(
SELECT /*id,id_awaria,poczatek_naprawy,koniec_naprawy, */
sum(zadanie.[dbo].[getMinutesFromDates] (poczatek_naprawy, koniec_naprawy))
FROM @tmp_table_base
)
return @time

END
GO


/****** Object:  StoredProcedure [dbo].[SumOfAllInactiveMinutes]    Script Date: 16.01.2023 23:29:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
CREATE procedure [dbo].[SumOfAllInactiveMinutes] 
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

SET @Overal_sum = @individual_sum
--SELECT @overal_sum

FETCH NEXT FROM kursor INTO @id

END
CLOSE kursor
DEALLOCATE kursor

SELECT @overal_sum

END

GO
