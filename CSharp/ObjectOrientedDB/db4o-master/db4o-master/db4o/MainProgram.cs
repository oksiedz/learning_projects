using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Db4objects.Db4o;
using Idbo;


namespace db4o
{
    public class MainProgram
    {
        public static void ListTickets(List<Ticket> result)
        {
            Console.WriteLine(result.Count);
            foreach (var item in result)
            {
                try
                {
                    Console.WriteLine("Guide: " + item.Unique_guid);
                    Console.WriteLine("Subject: " + item.subject);
                    Console.WriteLine("Description: " + item.Description);
                    Console.WriteLine("Priority: " + item.priority);
                    Console.WriteLine("Creation date: " + item.creation_date);
                    Console.WriteLine("Closing date: " + item.closing_date);
                    Console.WriteLine("Labels: " + item.Label);
                    Console.WriteLine("Expected update date: " + item.Expected_update_date);
                    Console.WriteLine("Comments:");
                    if (item.Comments != null)
                    {
                        foreach (var itemCom in item.Comments)
                        {
                            Console.WriteLine("Date: " + itemCom.Date);
                            Console.WriteLine("Content: " + itemCom.Text);
                            Console.WriteLine("Attachments for comments:");
                            if (itemCom.Attachments != null)
                            {
                                foreach (var itemAttach in itemCom.Attachments)
                                {
                                    Console.WriteLine("Date: " + itemAttach.Date);
                                    Console.WriteLine("Attachment: " + itemAttach.Object);
                                }
                            }
                        }
                    }
                    Console.WriteLine("Attachments to the ticket:");
                    if (item.Attachments != null)
                    {
                        foreach (var itemTicketAttach in item.Attachments)
                        {
                            Console.WriteLine("Date: " + itemTicketAttach.Date);
                            Console.WriteLine("Attachment: " + itemTicketAttach.Object);
                        }
                    }
                }
                catch
                { }
                Console.WriteLine();
            }
        }
        public static void ListAuditors(List<Auditor> result)
        {
            Console.WriteLine(result.Count);
            foreach (var item in result)
            {
                try
                {
                    Console.WriteLine("Full name: " + item.Full_name);
                    Console.WriteLine("Login: " + item.Login);
                    Console.WriteLine("Position: " + item.position);
                    Console.WriteLine("Is Active: " + item.is_active);
                    Console.WriteLine("Password: " + item.Password);
                }
                catch
                { }
                Console.WriteLine();
            }
        }
        public static void exit()
        {
            Console.Clear();
            Environment.Exit(0);
        }
        static void Main(string[] args)
        {
            ConsoleKeyInfo cki;
            do
            {
                Console.Clear();
                Console.WriteLine("Welcome:");
                Console.WriteLine("==============");
                Console.WriteLine();
                Console.WriteLine("0 -> List all tickets");
                Console.WriteLine("1 -> Add new ticket");
                Console.WriteLine("2 -> Search for ticket");
                Console.WriteLine("3 -> Update ticket");
                Console.WriteLine("4 -> Add comment to the ticket");
                Console.WriteLine("5 -> Add attachment to the ticket");
                Console.WriteLine("6 -> Add Auditor");
                Console.WriteLine("7 -> Activate auditor");
                Console.WriteLine("8 -> List auditors");
                Console.WriteLine("9 -> Exit");
                Console.WriteLine();

                IObjectContainer db = Db4oEmbedded.OpenFile(Db4oEmbedded.NewConfiguration(), "Database");

                cki = Console.ReadKey();

                if (cki.Key == ConsoleKey.D0) //presentation of tickets
                {
                    try
                    {
                        Console.Clear();
                        var tickets = db.Query<Ticket>().ToList();
                        ListTickets(tickets);
                        Console.WriteLine();
                        Console.WriteLine("Press ENTER to go back to menu.");
                        Console.ReadLine();
                        db.Close();
                    }
                    finally
                    {
                        db.Close();
                    }
                }

                else if (cki.Key == ConsoleKey.D1) //add ticket
                {
                    var ticket = new Ticket();
                    Console.Clear();
                    Console.Write("Subject:\n");
                    ticket.subject = Console.ReadLine();
                    Console.Write("Description: \n");
                    ticket.Description = Console.ReadLine();
                    ticket.creation_date = DateTime.Now;
                    Guid guid = Guid.NewGuid();
                    ticket.Unique_guid = guid.ToString();
                    Console.Write("Ticket Identifier: " + ticket.Unique_guid);

                    try
                    {
                        db.Store(ticket);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Ticket was added to the data base");
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Ticket was not created");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }
                }

                else if (cki.Key == ConsoleKey.D2) //search for ticket
                {
                    Console.Clear();
                    var ticket = new Ticket();
                    Console.WriteLine("Put the UniqueIdenifier of the ticket:");
                    ticket.Unique_guid = Console.ReadLine();
                    
                    var tickets = db.Query<Ticket>(x => x.Unique_guid == ticket.Unique_guid).ToList();

                    ListTickets(tickets);
                    Console.WriteLine();
                    Console.WriteLine("Press enter to go back to menu.");
                    Console.ReadLine();
                    db.Close();
                }

                else if (cki.Key == ConsoleKey.D3) //update
                {
                    Console.Clear();
                    var ticket = new Ticket();
                    Console.WriteLine("Put the UniqueIdentifier of the ticket:");
                    ticket.Unique_guid = Console.ReadLine();


                    var tickets = db.Query<Ticket>(x => x.Unique_guid == ticket.Unique_guid).ToList();
                    ListTickets(tickets);
                    Console.WriteLine();

                    Ticket t = tickets.First();
                    
                    Console.Write("Press T to change label\n");
                    ConsoleKeyInfo yesNo = Console.ReadKey();
                    if (yesNo.Key == ConsoleKey.T)
                    {
                        Console.Write("Write new label:\n");
                        if (t.Label == null)
                        {
                            t.Label = Console.ReadLine();
                        }
                        else
                        {
                            t.Label = t.Label + "," + Console.ReadLine();
                        }
                    }
                    Console.Write("Press T to change priority");
                    yesNo = Console.ReadKey();
                    if (yesNo.Key == ConsoleKey.T)
                    {
                        Console.Write("Set new priority:\n");
                        t.priority = int.Parse(Console.ReadLine());
                    }
                    Console.Write("Press T to change Expected update date");
                    yesNo = Console.ReadKey();
                    if (yesNo.Key == ConsoleKey.T)
                    {
                        Console.Write("Set new Expected update date (YYYY-MM-DD):\n");
                        t.Expected_update_date = DateTime.Parse(Console.ReadLine());
                    }
                    try
                    {
                        db.Store(t);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Data were udpated properly. Returning to menu.");
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Data were not updated.");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }
                }
                else if (cki.Key == ConsoleKey.D4) //add comment to the ticket
                {
                    Console.Clear();
                    var ticket = new Ticket();
                    Console.WriteLine("Put the UniqueIdentifier of the ticket:");
                    ticket.Unique_guid = Console.ReadLine();


                    var tickets = db.Query<Ticket>(x => x.Unique_guid == ticket.Unique_guid).ToList();
                    ListTickets(tickets);
                    Console.WriteLine();

                    Ticket t = tickets.First();
                    Console.WriteLine("Write please the comment below:");
                    var Comment = new Comment();
                    Comment.Text = Console.ReadLine();
                    Comment.Date = DateTime.Now;
                    
                    if (t.Comments == null)
                    {
                        t.Comments = new List<Comment>();
                    }
                    t.Comments.Add(Comment);
                    ConsoleKeyInfo yesNo = Console.ReadKey();
                    do
                    {
                        if (yesNo.Key != ConsoleKey.N)
                        {
                            Console.WriteLine("\nDo you want to add attachment? [T/N]");
                            yesNo = Console.ReadKey();
                            if (yesNo.Key == ConsoleKey.T)
                            {
                                var attachment = new Attachment();
                                Console.WriteLine("\n\nAdd attachment:");
                                attachment.Object = Console.ReadLine();
                                attachment.Date = DateTime.Now;
                                if (Comment.Attachments == null)
                                {
                                    Comment.Attachments = new List<Attachment>();
                                }
                                Comment.Attachments.Add(attachment);
                            }
                        }
                    } while (yesNo.Key != ConsoleKey.N);
                    try
                    {
                        db.Store(t);
                        db.Store(t.Comments);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Comment was added.");
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Comment was not added properly.");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }

                }
                else if (cki.Key == ConsoleKey.D5) //add attachment to the ticket
                {
                    Console.Clear();
                    var ticket = new Ticket();
                    Console.WriteLine("Put the UniqueIdentifier of the ticket:");
                    ticket.Unique_guid = Console.ReadLine();


                    var tickets = db.Query<Ticket>(x => x.Unique_guid == ticket.Unique_guid).ToList();
                    ListTickets(tickets);
                    Console.WriteLine();

                    Ticket t = tickets.First();
                    Console.WriteLine("Write please the attachment below:");
                    var Attachment = new Attachment();
                    Attachment.Object = Console.ReadLine();
                    Attachment.Date = DateTime.Now;

                    if (t.Attachments == null)
                    {
                        t.Attachments = new List<Attachment>();
                    }
                    t.Attachments.Add(Attachment);
                    try
                    {
                        db.Store(t);
                        db.Store(t.Attachments);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Attachment was added.");
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Attachment was not added properly.");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }

                }
                else if (cki.Key == ConsoleKey.D6) //add auditor
                {
                    Console.Clear();
                    var auditor = new Auditor();
                    Console.Write("Full name:\n");
                    auditor.Full_name = Console.ReadLine();
                    Console.Write("Login: \n");
                    auditor.Login = Console.ReadLine();
                    Console.Write("Position: \n");
                    auditor.position = Console.ReadLine();
                    auditor.is_active = false;
                    Guid guid = Guid.NewGuid();
                    auditor.Password = guid.ToString();

                    try
                    {
                        db.Store(auditor);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Auditor was added to the data base");
                        Console.WriteLine("login: " + auditor.Login + ", password: " + auditor.Password);
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Auditor was not added.");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }

                }
                else if (cki.Key == ConsoleKey.D7) //activate auditor
                {
                    Console.Clear();
                    var auditor = new Auditor();
                    Console.WriteLine("Put the login of the auditor:");
                    auditor.Login = Console.ReadLine();


                    var auditors = db.Query<Auditor>(x => x.Login == auditor.Login).ToList();

                    ListAuditors(auditors);
                    Console.WriteLine();

                    Auditor t = auditors.First();

                    t.is_active = true;
                    try
                    {
                        db.Store(t);
                        db.Commit();
                        Console.WriteLine();
                        Console.WriteLine("Auditor with login " + t.Login + " was activated.");
                        Console.ReadLine();
                        db.Close();
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Auditor was not activated.");
                        Console.WriteLine(e);
                        Console.ReadLine();
                    }

                    finally
                    {
                        db.Close();
                    }

                }
                else if (cki.Key == ConsoleKey.D8) //list auditors
                {
                    try
                    {
                        Console.Clear();
                        var auditors = db.Query<Auditor>().ToList();
                        ListAuditors(auditors);
                        Console.WriteLine();
                        Console.WriteLine("Press ENTER to go back to menu.");
                        Console.ReadLine();
                        db.Close();
                    }
                    finally
                    {
                        db.Close();
                    }

                }
                db.Close();
            } while (cki.Key != ConsoleKey.D9);

            exit();


            //IObjectContainer db = Db4oEmbedded.OpenFile(Db4oEmbedded.NewConfiguration(), "person.data");
            //try
            //{

            //    //Person stefan = new Person("Max", "Mucha", 25);
            //    //Person halina = new Person("Min", "Komar", 26);

            //    //db.Store(stefan);
            //    //db.Store(halina);

            //    IObjectSet osoby = db.QueryByExample(new Person(null, null, 0));
            //    IObjectSet result = db.QueryByExample(osoby);
            //    ListResult(osoby);



            //    Console.Read();
            //}
            //finally
            //{
            //    db.Close();
            //}
        }


    }
}
