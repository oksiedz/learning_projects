/****** Object:  StoredProcedure [dbo].[Number_of_shifts_not_working]    Script Date: 18.01.2023 22:36:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[Number_of_shifts_not_working]
(	@data1 datetime,
	@data2 datetime,
	@deviceid int
)
as
begin
DECLARE @t table (id int, id_awaria int, poczatek_naprawy datetime, koniec_naprawy datetime)
INSERT @t
EXEC zadanie.[dbo].[getAgregateIntervals] @data1, @data2, @deviceid

SELECT id,poczatek_naprawy, koniec_naprawy, zadanie.dbo.getshiftsfromdates(poczatek_naprawy, koniec_naprawy) Number_of_shifts
From @t


end
GO


/****** Object:  StoredProcedure [dbo].[SumOfInactiveMinutes]    Script Date: 18.01.2023 22:36:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date, ,>
-- Description:	<Description, ,>
-- =============================================
ALTER procedure [dbo].[SumOfInactiveMinutes] 
(
	-- Add the parameters for the function here
	@data1 datetime,
	@data2 datetime,
	@deviceid int,
	@ifreturn int
)
AS
BEGIN
	
	declare
	@tmp_table_base table (id int, id_awaria int, poczatek_naprawy datetime, koniec_naprawy datetime)
	INSERT INTO @tmp_table_base
(
    id, id_awaria, poczatek_naprawy, koniec_naprawy)
EXEC zadanie.[dbo].[getAgregateIntervals] @data1, @data2, @deviceid



IF @ifreturn = 1
BEGIN 
return (
        SELECT /*id,id_awaria,poczatek_naprawy,koniec_naprawy, */
               sum(zadanie.[dbo].[getMinutesFromDates] (poczatek_naprawy, koniec_naprawy))
        FROM @tmp_table_base
)
END
ELSE
BEGIN
SELECT /*id,id_awaria,poczatek_naprawy,koniec_naprawy, */
       sum(zadanie.[dbo].[getMinutesFromDates] (poczatek_naprawy, koniec_naprawy))
FROM @tmp_table_base
END

END
GO






/****** Object:  StoredProcedure [dbo].[SumOfAllInactiveMinutes]    Script Date: 18.01.2023 22:36:29 ******/
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

exec @individual_sum = zadanie.dbo.SumOfInactiveMinutes @data1=@date_from, @data2=@date_to, @deviceid=@id, @ifreturn = 1

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
ALTER procedure [dbo].[Unit_with_longest_malfunctions] 
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

DROP PROCEDURE zadanie.dbo.SumOfInactiveMinutes2


