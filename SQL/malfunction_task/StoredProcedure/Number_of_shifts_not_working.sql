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