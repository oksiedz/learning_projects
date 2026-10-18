using System;

/// <summary>
/// Summary description for Class1
/// </summary>
/// 
namespace db4o
{
	public abstract class User
	{
		public string Full_name { get; set; }
		public string Login { get; set; }
		public Boolean is_active {get; set;}
		public string Password { get; set; }

		public void add_attachment()
		{
			Console.WriteLine("Attachment added");
		}

		public void add_comment()
		{
			Console.WriteLine("Comment added");
		}

		public void add_ticket()
		{
			Console.WriteLine("Ticket added");
		}
		public void login()
		{
			Console.WriteLine("Logged in");
		}

		public void logout()
		{
			Console.WriteLine("Logged out");
		}

		public void open_menu()
		{
			Console.WriteLine("Menu opened");
		}
	}
}