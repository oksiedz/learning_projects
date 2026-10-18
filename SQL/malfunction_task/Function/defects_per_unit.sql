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