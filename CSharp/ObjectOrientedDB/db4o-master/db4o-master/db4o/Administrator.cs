using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Administrator : User
    {
        public void activate_user()
        {
            Console.WriteLine("User activated");
        }

        public void block_user()
        {
            Console.WriteLine("User blocked");
        }

        public void create_user()
        {
            Console.WriteLine("User created");
        }

        public void manage_user()
        {
            Console.WriteLine("User managed");
        }

        public void restart_user_password()
        {
            Console.WriteLine("Password reseted");
        }
    }
}
