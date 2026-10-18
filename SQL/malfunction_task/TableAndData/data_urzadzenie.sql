SET IDENTITY_INSERT [dbo].[urzadzenie] ON 

INSERT [dbo].[urzadzenie] ([id], [oddzial_id], [nazwa], [status], [nr_seryjny]) VALUES (1, 1, N'Drukarka XYZ 1', 1, N'1234AB')
INSERT [dbo].[urzadzenie] ([id], [oddzial_id], [nazwa], [status], [nr_seryjny]) VALUES (2, 1, N'Drukarka XYZ 2', 1, N'3456AC')
INSERT [dbo].[urzadzenie] ([id], [oddzial_id], [nazwa], [status], [nr_seryjny]) VALUES (3, 2, N'Wtryskarka XYZ 1', 1, N'2345CD')
INSERT [dbo].[urzadzenie] ([id], [oddzial_id], [nazwa], [status], [nr_seryjny]) VALUES (4, 2, N'Wtryskarka XYZ 2', 1, N'4567DE')
SET IDENTITY_INSERT [dbo].[urzadzenie] OFF
GO