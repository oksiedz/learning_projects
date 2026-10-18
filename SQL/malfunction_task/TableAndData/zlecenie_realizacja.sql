/****** Object:  Table [dbo].[zlecenie_realizacja]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zlecenie_realizacja](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[oddzial_id] [int] NULL,
	[pracownik_id] [int] NULL,
	[zlecenie_id] [int] NULL,
	[zlecenie_poczatek] [datetime] NULL,
	[zlecenie_koniec] [datetime] NULL,
	[zlecenie_status] [int] NULL,
	[zlecenie_estymata_id] [int] NULL,
	[status_id] [int] NULL,
 CONSTRAINT [PK__zlecenie__3213E83F4FAD5E68] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[zlecenie_realizacja]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_realizacja_estymata] FOREIGN KEY([zlecenie_estymata_id])
REFERENCES [dbo].[estymata] ([id])
GO
ALTER TABLE [dbo].[zlecenie_realizacja] CHECK CONSTRAINT [FK_zlecenie_realizacja_estymata]
GO
ALTER TABLE [dbo].[zlecenie_realizacja]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_realizacja_oddzial] FOREIGN KEY([oddzial_id])
REFERENCES [dbo].[oddzial] ([id])
GO
ALTER TABLE [dbo].[zlecenie_realizacja] CHECK CONSTRAINT [FK_zlecenie_realizacja_oddzial]
GO
ALTER TABLE [dbo].[zlecenie_realizacja]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_realizacja_pracownik] FOREIGN KEY([pracownik_id])
REFERENCES [dbo].[pracownik] ([id])
GO
ALTER TABLE [dbo].[zlecenie_realizacja] CHECK CONSTRAINT [FK_zlecenie_realizacja_pracownik]
GO
ALTER TABLE [dbo].[zlecenie_realizacja]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_realizacja_zlecenia] FOREIGN KEY([zlecenie_id])
REFERENCES [dbo].[zlecenia] ([id])
GO
ALTER TABLE [dbo].[zlecenie_realizacja] CHECK CONSTRAINT [FK_zlecenie_realizacja_zlecenia]
GO
ALTER TABLE [dbo].[zlecenie_realizacja]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_realizacja_zlecenie_status] FOREIGN KEY([status_id])
REFERENCES [dbo].[zlecenie_status] ([id])
GO
ALTER TABLE [dbo].[zlecenie_realizacja] CHECK CONSTRAINT [FK_zlecenie_realizacja_zlecenie_status]
GO