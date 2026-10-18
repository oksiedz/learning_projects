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