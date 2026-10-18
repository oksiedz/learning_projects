/****** Object:  Table [dbo].[zlecenia]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zlecenia](
	[id_zlecenia] [int] IDENTITY(1,1) NOT NULL,
	[numer_zlecenia] [varchar](255) NULL,
	[data_zlecenia] [datetime] NULL,
	[oddzial_id] [int] NULL,
 CONSTRAINT [PK__zlecenia__3213E83F808F5DE0] PRIMARY KEY CLUSTERED 
(
	[id_zlecenia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[zlecenia]  WITH CHECK ADD  CONSTRAINT [FK_zlecenia_oddzial] FOREIGN KEY([oddzial_id])
REFERENCES [dbo].[oddzial] ([id])
GO
ALTER TABLE [dbo].[zlecenia] CHECK CONSTRAINT [FK_zlecenia_oddzial]
GO