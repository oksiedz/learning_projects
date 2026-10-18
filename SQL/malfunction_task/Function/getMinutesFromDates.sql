SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
--Create function getMinutesFromDates (@data1 datetime, @data2 datetime) returns int
CREATE function [dbo].[getMinutesFromDates] (@data1 datetime, @data2 datetime) returns int
as
begin

declare @result int;
declare @dayOfWeek1 int;
declare @dayOfWeek2 int;
declare @pom int; -- pomocnicza
declare @pom_date1 datetime; -- pomocnicza
declare @pom_result nvarchar(max)
declare @weeks int 

--	set @data1 = convert(datetime,'2022-11-19 12:54:12', 102)
--	set @data2 = convert(datetime,'2022-11-30 15:54:12', 102)

	set @dayOfWeek1 = datepart(WEEKDAY, @data1); -- odczytanie dnia tygodnia z daty1
--	if (@dayOfWeek1=7 and datepart(hour, @data1)>=6) -- jesli sobota i po 6.00 to przesuwamy sie z data na koniec dnia
--	  begin
--		set @pom = Datediff(n, @data1, (convert(datetime,	convert(varchar(4), datepart(YYYY, @data1)) + '-'+
--															convert(varchar(2), datepart(mm, @data1))+ '-'+
--															convert(varchar(2), datepart(dd, @data1))+' 23:59:59', 102) ));
--		set @pom = @pom + 30*60; -- przesywamy sie na 6.00 w poniedzialek
--	  end;
--	if (@dayOfWeek1=2 and datepart(hour, @data1)<6) -- jeli poniedzialek przed 6.00
--		begin
--		set @pom = Datediff(n, @data1, (convert(datetime,	convert(varchar(4), datepart(YYYY, @data1)) + '-'+
--															convert(varchar(2), datepart(mm, @data1))+ '-'+
--															convert(varchar(2), datepart(dd, @data1))+' 06:00:00', 102) ));
--		end;
--	if (@dayOfWeek1=1 ) -- jeli niedziela
--		begin
--		set @pom = Datediff(n, @data1, (convert(datetime,	convert(varchar(4), datepart(YYYY, @data1)) + '-'+
--															convert(varchar(2), datepart(mm, @data1))+ '-'+
--															convert(varchar(2), datepart(dd, @data1))+' 23:59:59', 102) ));
--		set @pom = @pom + 6*60; -- przesywamy sie na 6.00 w poniedzialek
--		end;
--
--	set @dayOfWeek2 = datepart(weekday, @data2);	
--	if (@dayOfWeek1 = 1 or @dayOfWeek1=7 and datepart(hour, @data1)>=6 or @dayOfWeek1=7 and datepart(hour, @data1)<6 )
--	set @data1

-- drugi wariant - upraszczajacy
	if 	(@dayOfWeek1=7 and datepart(hour, @data1)>=6) or
		(@dayOfWeek1=1 ) or
		(@dayOfWeek1=2 and datepart(hour, @data1)<6)
		begin
			if (@dayOfWeek1=7 and datepart(hour, @data1)>=6) -- jesli sobota i po 6.00 to przesuwamy sie z data na koniec dnia
			  begin
				set @data1 = dateadd (dd, 2, @data1);
			  end
			if (@dayOfWeek1=1 ) -- -- jeli niedziela
			  begin
				set @data1 = dateadd (dd, 1, @data1);
			  end
			set @data1 = convert(datetime,	convert(varchar(4), datepart(YYYY, @data1)) + '-'+
																convert(varchar(2), datepart(mm, @data1))+ '-'+
																convert(varchar(2), datepart(dd, @data1))+' 06:00:00', 102);
		end
	
	set @dayOfWeek2 = datepart(WEEKDAY, @data2); -- odczytanie dnia tygodnia z daty2
	if 	(@dayOfWeek2=7 and datepart(hour, @data2)>=6) or
		(@dayOfWeek2=1 ) or
		(@dayOfWeek2=2 and datepart(hour, @data2)<6)
		begin
			if (@dayOfWeek2=1 ) -- jeli niedziela
			  begin
				set @data2 = dateadd (dd, -1, @data2);
			  end
			if (@dayOfWeek2=2 and datepart(hour, @data2)<6) -- jeli poniedzialek
			  begin
				set @data2 = dateadd (dd, -2, @data2);
			  end
			set @data2 = convert(datetime,	convert(varchar(4), datepart(YYYY, @data2)) + '-'+
																convert(varchar(2), datepart(mm, @data2))+ '-'+
																convert(varchar(2), datepart(dd, @data2))+' 06:00:00', 102);
		end

		set @result = datediff(n, @data1, @data2);
			--if (@result /10080) -- ilosc minut w tygodniu

		
		set @weeks = DATEPART(ww,@data2)-  DATEPART(ww,@data1)
		set @result = @result - (@weeks * 2880) -- jesli weekend wystepuje w czasie naprawy.

return @result
end;
GO