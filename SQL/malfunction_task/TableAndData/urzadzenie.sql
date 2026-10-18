/****** Object:  Table [dbo].[urzadzenie]    Script Date: 17.12.2022 15:41:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[urzadzenie](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[oddzial_id] [int] NULL,
	[nazwa] [varchar](255) NULL,
	[status] [int] NULL,
	[nr_seryjny] [varchar](100) NULL,
 CONSTRAINT [PK__urzadzen__3213E83F5F8B800F] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[urzadzenie]  WITH CHECK ADD  CONSTRAINT [FK_urzadzenie_oddzial] FOREIGN KEY([oddzial_id])
REFERENCES [dbo].[oddzial] ([id])
GO
ALTER TABLE [dbo].[urzadzenie] CHECK CONSTRAINT [FK_urzadzenie_oddzial]
GO
ALTER TABLE [dbo].[urzadzenie]  WITH CHECK ADD  CONSTRAINT [FK_urzadzenie_urzadzenie_status] FOREIGN KEY([status])
REFERENCES [dbo].[urzadzenie_status] ([id])
GO
ALTER TABLE [dbo].[urzadzenie] CHECK CONSTRAINT [FK_urzadzenie_urzadzenie_status]
GO