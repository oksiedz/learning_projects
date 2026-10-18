/****** Object:  UserDefinedFunction [dbo].[getShiftsFromDates]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
--Create function getMinutesFromDates (@data1 datetime, @data2 datetime) returns int
CREATE function [dbo].[getShiftsFromDates] (@data1 datetime, @data2 datetime) returns int
as
begin

declare @result int;
declare @dayOfWeek1 int;
declare @dayOfWeek2 int;
declare @pom int; -- pomocnicza
declare @pom_date1 datetime; -- pomocnicza
declare @pom_result nvarchar(max)
declare @weeks int 

	set @dayOfWeek1 = datepart(WEEKDAY, @data1); -- odczytanie dnia tygodnia z daty1

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

		DECLARE @jumpdatetime datetime = @data1
		DECLARE @shift_number int = 0
		WHILE @jumpdatetime < @data2
		BEGIN
		--sobota 7
		--niedziela 1
		--poniedziałek 2
		--datepart(hour, @data1)
		/*if kiedy weekend*/
			IF (datepart(WEEKDAY, @jumpdatetime)=7 and datepart(hour, @jumpdatetime)>=6) OR (datepart(WEEKDAY, @jumpdatetime)=1) OR
			(datepart(WEEKDAY, @jumpdatetime)=2 and datepart(hour, @jumpdatetime)<6)
			BEGIN
				SET @shift_number = @shift_number
			END
			ELSE 
				SET @shift_number = @shift_number + 1
			
			SET @jumpdatetime = dateadd(hour, 8, @jumpdatetime)
		END

		SET @shift_number = CASE WHEN zadanie.dbo.shift_no(@jumpdatetime) = zadanie.dbo.shift_no(@data2) THEN @shift_number + 1 ELSE @shift_number END


return @shift_number
end;
GO