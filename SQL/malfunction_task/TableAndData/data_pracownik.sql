SET IDENTITY_INSERT [dbo].[pracownik] ON 

INSERT [dbo].[pracownik] ([id], [oddzial_id], [nazwa]) VALUES (1, 1, N'Adam Kowalski')
INSERT [dbo].[pracownik] ([id], [oddzial_id], [nazwa]) VALUES (2, 1, N'Tomasz Testowy')
INSERT [dbo].[pracownik] ([id], [oddzial_id], [nazwa]) VALUES (3, 2, N'Jan Berg')
INSERT [dbo].[pracownik] ([id], [oddzial_id], [nazwa]) VALUES (4, 2, N'Piotr Drugi')
SET IDENTITY_INSERT [dbo].[pracownik] OFF
GO