using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace db4o
{
    public class Ticket
    {
        public string change_log { get; set; }
        public DateTime closing_date { get; set; }
        public DateTime creation_date { get; set; }
        public string Description;
        public DateTime Expected_update_date;
        public string Label;
        public int priority;
        public string subject;
        private string unique_guid;
        public string Unique_guid { get; set; }
        public List<Comment> Comments;
        public List<Attachment> Attachments;
        public Department Department;
        public Category Category;
        public void add_estimated_end_time()
        {
            Console.WriteLine("Estimated end time updated");
        }
        public void register_ticket()
        {
            Console.WriteLine("Ticket registered");
        }
        public void set_status()
        {
            Console.WriteLine("Status set");
        }
    }
}
