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
CREATE procedure [dbo].[SumOfInactiveMinutes] 
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