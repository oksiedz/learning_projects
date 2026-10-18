Drop table zadanie.dbo.estymata;
drop table zadanie.dbo.firma;


DROP TABLE zadanie.dbo.zlecenia;	
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



/****** Object:  Table [dbo].[zlecenie_element_status]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zlecenie_element_status](
	[id_zlecenie_status] [int] IDENTITY(1,1) NOT NULL,
	[zlecenie_status] [varchar](50) NULL,
 CONSTRAINT [PK_zlecenie_status] PRIMARY KEY CLUSTERED 
(
	[id_zlecenie_status] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

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

/****** Object:  Table [dbo].[element_typ]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[element_typ](
	[id_typ] [int] IDENTITY(1,1) NOT NULL,
	[typ_name] [nvarchar](255) NOT NULL,
	[typ_time_min] [int] NOT NULL,
 CONSTRAINT [PK_element_typ] PRIMARY KEY CLUSTERED 
(
	[id_typ] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

SET IDENTITY_INSERT [dbo].[zlecenie_element_status] ON 

INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (1, N'To Do')
INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (2, N'In Progress')
INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (3, N'Done')
SET IDENTITY_INSERT [dbo].[zlecenie_element_status] OFF
GO


SET IDENTITY_INSERT [dbo].[zlecenia] ON 

INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (1, N'ZLEC1', CAST(N'2010-01-01T00:00:00.000' AS DateTime), 1)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (2, N'ZLEC2', CAST(N'2010-01-02T00:00:00.000' AS DateTime), 1)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (3, N'ZLEC3', CAST(N'2010-01-03T00:00:00.000' AS DateTime), 1)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (4, N'ZLEC4', CAST(N'2010-01-04T00:00:00.000' AS DateTime), 1)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (5, N'ZLEC5', CAST(N'2010-01-05T00:00:00.000' AS DateTime), 1)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (6, N'ZLEC6', CAST(N'2010-01-06T00:00:00.000' AS DateTime), 2)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (7, N'ZLEC7', CAST(N'2010-01-07T00:00:00.000' AS DateTime), 2)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (8, N'ZLEC8', CAST(N'2010-01-08T00:00:00.000' AS DateTime), 2)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (9, N'ZLEC9', CAST(N'2010-01-09T00:00:00.000' AS DateTime), 2)
INSERT [dbo].[zlecenia] ([id_zlecenia], [numer_zlecenia], [data_zlecenia], [oddzial_id]) VALUES (10, N'ZLEC10', CAST(N'2010-01-09T00:00:00.000' AS DateTime), 2)
SET IDENTITY_INSERT [dbo].[zlecenia] OFF
GO



SET IDENTITY_INSERT [dbo].[zlecenie_element] ON 

INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (1, 1, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (2, 1, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (3, 2, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (4, 2, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (5, 3, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (6, 3, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (7, 4, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (8, 4, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (9, 5, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (10, 5, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (11, 6, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (12, 6, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (13, 7, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (14, 7, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (15, 8, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (16, 8, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (17, 9, 2, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (18, 9, 3, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (19, 10, 1, 1, NULL, NULL, NULL)
INSERT [dbo].[zlecenie_element] ([id_zlecenie_element], [id_zlecenie], [id_type], [id_status], [id_urzadzenia], [realization_start], [realization_end]) VALUES (20, 10, 2, 1, NULL, NULL, NULL)
SET IDENTITY_INSERT [dbo].[zlecenie_element] OFF
GO

ALTER TABLE [dbo].[zlecenia]  WITH CHECK ADD  CONSTRAINT [FK_zlecenia_oddzial] FOREIGN KEY([oddzial_id])
REFERENCES [dbo].[oddzial] ([id])
GO
ALTER TABLE [dbo].[zlecenia] CHECK CONSTRAINT [FK_zlecenia_oddzial]
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





/****** Object:  View [dbo].[v_nieskonczone_zlecenia]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [dbo].[v_nieskonczone_zlecenia] AS 
SELECT a.oddzial_id, count(DISTINCT numer_zlecenia) as nieskonczone_zlecenia
FROM zadanie.dbo.zlecenia a
INNER JOIN zadanie.dbo.zlecenie_element b
ON id_zlecenia=b.id_zlecenie
INNER JOIN zadanie.dbo.zlecenie_element_status c
ON b.id_status=c.id_zlecenie_status
WHERE c.zlecenie_Status in ('To Do','In Progress')
group by a.oddzial_id
GO


/****** Object:  View [dbo].[v_elementy_do_realizacji_aggr]    Script Date: 21.01.2023 15:13:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE view [dbo].[v_elementy_do_realizacji_aggr] AS 
SELECT a.oddzial_id,count(id_zlecenie_element) liczba_Elementow_do_realizacji,sum(typ_time_min) czas_drukowania_elementow_do_realizacji_in_min
FROM zadanie.dbo.zlecenia a
INNER JOIN zadanie.dbo.zlecenie_element b
ON id_zlecenia=b.id_zlecenie
INNER JOIN zadanie.dbo.zlecenie_element_status c
ON b.id_status=c.id_zlecenie_status
INNER JOIN element_typ d
ON b.id_type = d.id_typ
WHERE c.zlecenie_Status in ('To Do')
group by a.oddzial_id
GO


