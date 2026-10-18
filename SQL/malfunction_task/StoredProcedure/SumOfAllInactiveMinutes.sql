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