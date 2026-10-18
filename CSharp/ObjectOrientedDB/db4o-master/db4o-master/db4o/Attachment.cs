using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Attachment
    {
        public DateTime Date { get; set; }
        public string Object;
        public void load_object()
        {
            Console.WriteLine("Object loaded");
        }

        public void show_attachment()
        {
            Console.WriteLine("Attachment showed");
        }
    }
}
