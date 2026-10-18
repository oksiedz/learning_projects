using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
	public class Auditor : User
	{
		public string position { get; set; }


		public void add_ticket_label()
		{
			Console.WriteLine("Label Added");
		}

		public void change_ticket_Status()
        {
			Console.WriteLine("Status changed");
        }

		public void change_attribute_ticket()
        {
			Console.WriteLine("Attribute changed");
        }

		public void export_ticket()
        {
			Console.WriteLine("Ticket exported");
        }

		public void filter_ticket_list()
        {
			Console.WriteLine("Ticket's list exported");
        }

		public void view_ticket()
        {
			Console.WriteLine("Ticket viewed");
        }
	}
}
