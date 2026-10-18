/****** Object:  Table [dbo].[usterka]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usterka](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_awaria] [int] NULL,
	[opis] [varchar](1000) NULL,
	[data_zgloszenia] [datetime] NULL,
	[poczatek_naprawy] [datetime] NULL,
	[koniec_naprawy] [datetime] NULL,
	[urzadzenie_id] [int] NOT NULL,
	[status_id] [int] NULL,
 CONSTRAINT [PK__usterka__3213E83FE385BEAB] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[usterka]  WITH CHECK ADD  CONSTRAINT [FK_usterka_urzadzenie] FOREIGN KEY([urzadzenie_id])
REFERENCES [dbo].[urzadzenie] ([id])
GO
ALTER TABLE [dbo].[usterka] CHECK CONSTRAINT [FK_usterka_urzadzenie]
GO
ALTER TABLE [dbo].[usterka]  WITH CHECK ADD  CONSTRAINT [FK_usterka_usterka_status] FOREIGN KEY([status_id])
REFERENCES [dbo].[usterka_status] ([id])
GO
ALTER TABLE [dbo].[usterka] CHECK CONSTRAINT [FK_usterka_usterka_status]
GO