using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Category
    {
        public Boolean is_active { get; set; }
        public string main_name { get; set; }
        public string name { get; set; }
        public void add_category()
        {
            Console.WriteLine("Category added");
        }

        public void modify_category()
        {
            Console.WriteLine("Category modified");
        }
    }
}
