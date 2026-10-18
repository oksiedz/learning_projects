SET IDENTITY_INSERT [dbo].[usterka_status] ON 

INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (1, N'urządzenie działa poprawnie')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (2, N'przekazanie informacji do centrali')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (3, N'diagnoza przyczyny awarii')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (4, N'rozpoczęcie naprawy')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (5, N'testy')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (6, N'przywrócenie do etapu działania produkcyjnego')
INSERT [dbo].[usterka_status] ([id], [opis]) VALUES (7, N'urządzenia nie udaje się naprawić podlega kasacji')
SET IDENTITY_INSERT [dbo].[usterka_status] OFF
GO