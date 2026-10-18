using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Comment
    {
        public DateTime Date { get; set; }
        public string Text { get; set; }
        public List<Attachment> Attachments { get; set; }

        public void register_comment()
        {
            Console.WriteLine("Comment registered");
        }

        public void show_comment()
        {
            Console.WriteLine("Comment showed");
        }
    }
}
