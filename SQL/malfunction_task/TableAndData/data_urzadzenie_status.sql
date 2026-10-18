SET IDENTITY_INSERT [dbo].[urzadzenie_status] ON 

INSERT [dbo].[urzadzenie_status] ([id], [status], [opis]) VALUES (1, 0, N'Active')
INSERT [dbo].[urzadzenie_status] ([id], [status], [opis]) VALUES (2, 1, N'Inactive')
SET IDENTITY_INSERT [dbo].[urzadzenie_status] OFF
GO