using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Notifier : User
    {
        public string Full_name = null;
        public string login = null;
        public string password = null;

        public void choose_category()
        {
            Console.WriteLine("Category choosen");
        }

        public void choose_department()
        {
            Console.WriteLine("Department choosen");
        }

        public void login_ticket (string uniqueidentifier)
        {
            Console.WriteLine("Logged into ticket");
        }
    }
}
