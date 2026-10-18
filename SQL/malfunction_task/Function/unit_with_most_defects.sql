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