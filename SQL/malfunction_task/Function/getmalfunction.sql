/****** Object:  UserDefinedFunction [dbo].[getmalfunction]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[getmalfunction]
(	
	@data1 datetime,
	@data2 datetime,
	@deviceid int
)
RETURNS TABLE 
AS
RETURN 
(
	-- Add the SELECT statement with parameter references here
	SELECT id, id_awaria, 
		iif (poczatek_naprawy < @data1, @data1, poczatek_naprawy) poczatek_naprawy,
		iif (koniec_naprawy > @data2 or koniec_naprawy is null, @data2, koniec_naprawy) koniec_naprawy
	from dbo.usterka where urzadzenie_id=@deviceid 
		--and (usterka.poczatek_naprawy >= @data1 and (usterka.koniec_naprawy <= @data2 or usterka.koniec_naprawy is null))
		and (
				(usterka.koniec_naprawy between @data1 and @data2 or usterka.koniec_naprawy is null)
				or (usterka.poczatek_naprawy between @data1 and @data2 and (usterka.koniec_naprawy is null or usterka.koniec_naprawy >= @data2))
				or (usterka.poczatek_naprawy<=@data1 and (usterka.koniec_naprawy is null or usterka.koniec_naprawy >= @data2))
			)
)

GO