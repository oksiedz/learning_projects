/****** Object:  Table [dbo].[zlecenie_element]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zlecenie_element](
	[id_zlecenie_element] [int] IDENTITY(1,1) NOT NULL,
	[id_zlecenie] [int] NOT NULL,
	[id_type] [int] NOT NULL,
	[id_status] [int] NOT NULL,
	[id_urzadzenia] [int] NULL,
	[realization_start] [datetime] NULL,
	[realization_end] [datetime] NULL,
 CONSTRAINT [PK_zlecenie_element] PRIMARY KEY CLUSTERED 
(
	[id_zlecenie_element] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[zlecenie_element]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_element_element_typ] FOREIGN KEY([id_type])
REFERENCES [dbo].[element_typ] ([id_typ])
GO
ALTER TABLE [dbo].[zlecenie_element] CHECK CONSTRAINT [FK_zlecenie_element_element_typ]
GO
ALTER TABLE [dbo].[zlecenie_element]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_element_urzadzenie] FOREIGN KEY([id_urzadzenia])
REFERENCES [dbo].[urzadzenie] ([id])
GO
ALTER TABLE [dbo].[zlecenie_element] CHECK CONSTRAINT [FK_zlecenie_element_urzadzenie]
GO
ALTER TABLE [dbo].[zlecenie_element]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_element_zlecenia] FOREIGN KEY([id_zlecenie])
REFERENCES [dbo].[zlecenia] ([id_zlecenia])
GO
ALTER TABLE [dbo].[zlecenie_element] CHECK CONSTRAINT [FK_zlecenie_element_zlecenia]
GO
ALTER TABLE [dbo].[zlecenie_element]  WITH CHECK ADD  CONSTRAINT [FK_zlecenie_element_zlecenie_element_status] FOREIGN KEY([id_status])
REFERENCES [dbo].[zlecenie_element_status] ([id_zlecenie_status])
GO
ALTER TABLE [dbo].[zlecenie_element] CHECK CONSTRAINT [FK_zlecenie_element_zlecenie_element_status]
GO