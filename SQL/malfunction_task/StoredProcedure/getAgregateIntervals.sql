/****** Object:  StoredProcedure [dbo].[getAgregateIntervals]    Script Date: 17.12.2022 15:41:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[getAgregateIntervals]
(	@data1 datetime,
	@data2 datetime,
	@deviceid int
)
as
begin
DECLARE @c1_id int,
	@c1_id_awaria int,
	@c1_poczatek_naprawy datetime,
	@c1_koniec_naprawy datetime,
	@c2_id int,
	@c2_id_awaria int,
	@c2_poczatek_naprawy datetime,
	@c2_koniec_naprawy datetime

	declare
	@tmp_table table (id int, id_awaria int, poczatek_naprawy datetime, koniec_naprawy datetime)
	declare
	@tmp_table_base table (id int, id_awaria int, poczatek_naprawy datetime, koniec_naprawy datetime)
	
	-- Add the SELECT statement with parameter references here
	INSERT INTO @tmp_table_base
	select * from getmalfunction(@data1, @data2, @deviceid);
	
	DECLARE @count1 int = 0
	DECLARE @count2 int = 1
	WHILE (@count1 <> @count2)
	BEGIN
		DELETE @tmp_table
		/*temporary*/
		--SELECT * from @tmp_table_base
		/*temporary*/
		declare c1 cursor for
			select * from @tmp_table_base order by id, koniec_naprawy;
		open c1
			fetch next from c1 into @c1_id, @c1_id_awaria, @c1_poczatek_naprawy, @c1_koniec_naprawy /*przechodzi po wszystkich wierszach*/
			WHILE @@FETCH_STATUS =0
			begin
				declare c2 cursor for
					select * from @tmp_table_base where id > @c1_id order by poczatek_naprawy, koniec_naprawy /*wszystkie kolejne wiersze z intervali*/;
					open c2
					fetch next from c2 into @c2_id, @c2_id_awaria, @c2_poczatek_naprawy, @c2_koniec_naprawy
					WHILE @@FETCH_STATUS = 0
					BEGIN
					if (@c2_poczatek_naprawy between @c1_poczatek_naprawy and @c1_koniec_naprawy) 
					   OR (@c1_poczatek_naprawy between @c2_poczatek_naprawy and @c2_koniec_naprawy)
					insert into @tmp_table (id, id_awaria, poczatek_naprawy, koniec_naprawy) values 
						(@c1_id, @c1_id_awaria, IIF(@c1_poczatek_naprawy < @c2_poczatek_naprawy, @c1_poczatek_naprawy, @c2_poczatek_naprawy)
						, IIF(@c1_koniec_naprawy > @c2_koniec_naprawy, @c1_koniec_naprawy, @c2_koniec_naprawy))
					fetch next from c2 into @c2_id, @c2_id_awaria, @c2_poczatek_naprawy, @c2_koniec_naprawy
					--PRINT('Petla')
					end
				close c2
				deallocate c2
				fetch next from c1 into @c1_id, @c1_id_awaria, @c1_poczatek_naprawy, @c1_koniec_naprawy
			end
		close c1
		deallocate c1
		SET @count1 = (SELECT count(1) FROM @tmp_table_base)
		SET @count2 = (SELECT count(1) FROM @tmp_table)
		--PRINT('count1:' + CONVERT(varchar(2),@count1)+'; count2:'+CONVERT(varchar(2),@count2))
		IF @count2 = 0
		BEGIN
		SET @count1 = @count2
		END
		
		IF (@count1 <> @count2 and @count2 <> 0)
		BEGIN
		DELETE FROM @tmp_table_base
		INSERT INTO @tmp_table_base
		SELECT * FROM @tmp_table
		END
		

	END

	select DISTINCT * from @tmp_table_base

end
GO