/****** Object:  Table [dbo].[pracownik]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[pracownik](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[oddzial_id] [int] NULL,
	[nazwa] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[pracownik]  WITH CHECK ADD  CONSTRAINT [FK_pracownik_oddzial] FOREIGN KEY([oddzial_id])
REFERENCES [dbo].[oddzial] ([id])
GO
ALTER TABLE [dbo].[pracownik] CHECK CONSTRAINT [FK_pracownik_oddzial]
GO