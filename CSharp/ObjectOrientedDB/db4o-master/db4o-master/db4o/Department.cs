using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Department
    {
        public string name { get; set; }
        public string office { get; set; }
        public void add_department()
        {
            Console.WriteLine("Department added.");
        }
        public void modify_department()
        {
            Console.WriteLine("Department modified");
        }
    }
}
