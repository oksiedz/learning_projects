/****** Object:  Table [dbo].[oddzial]    Script Date: 21.01.2023 23:51:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[oddzial](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nazwa] [varchar](255) NULL,
	[kod_oddzialu] [varchar](10) NULL,
	[brak_capacity] [tinyint] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO