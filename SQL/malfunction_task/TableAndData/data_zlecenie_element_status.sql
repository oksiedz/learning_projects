SET IDENTITY_INSERT [dbo].[zlecenie_element_status] ON 

INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (1, N'To Do')
INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (2, N'In Progress')
INSERT [dbo].[zlecenie_element_status] ([id_zlecenie_status], [zlecenie_status]) VALUES (3, N'Done')
SET IDENTITY_INSERT [dbo].[zlecenie_element_status] OFF
GO