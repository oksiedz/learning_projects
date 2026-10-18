using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SqlClient;

namespace AplikacjaBiblioteka
{
    public partial class issue_book : Form
    {
        //Connection string to the local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");
        public issue_book()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //Variable for row count
                int i = 0;

                //Select query
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select id, name, department, phone, email from student_info where index_no = '" + textBox1.Text + "'";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                i = Convert.ToInt32(dt.Rows.Count.ToString());

                if (i == 0)
                {
                    MessageBox.Show("Nie znaleziono studenta o numerze indeksu: " + textBox1.Text + "");
                }
                else
                {
                    foreach (DataRow dr in dt.Rows)
                    {
                        //Showing query otput in particular fields
                        textBox2.Text = dr["name"].ToString();
                        textBox3.Text = dr["department"].ToString();
                        textBox4.Text = dr["phone"].ToString();
                        textBox5.Text = dr["email"].ToString();
                        textBox7.Text = dr["id"].ToString();
                    }
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }

        }

        private void issue_book_Load(object sender, EventArgs e)
        {
            try
            {
                //Setting the connection
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void textBox6_KeyUp(object sender, KeyEventArgs e)
        {
            try
            {
                //Variable for count of results
                int count = 0;

                //Code to present the the books details while pressing whatever button (not enter)
                if (e.KeyCode != Keys.Enter)
                {
                    //Clearing the list
                    listBox1.Items.Clear();

                    //Query to the books details
                    SqlCommand cmd = con.CreateCommand();
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = "select * from book_info where name like '%" + textBox6.Text + "%'";
                    cmd.ExecuteNonQuery();
                    DataTable dt = new DataTable();
                    SqlDataAdapter da = new SqlDataAdapter(cmd);
                    da.Fill(dt);
                    count = Convert.ToInt32(dt.Rows.Count.ToString());

                    //Presenting the details if there are some results
                    if (count > 0)
                    {
                        listBox1.Visible = true;
                        
                        //Listing in listBox title and author of the book
                        foreach (DataRow dr in dt.Rows)
                        {
                            listBox1.Items.Add(dr["name"].ToString() + " - " + dr["author_name"].ToString());
                        }
                    }
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void textBox6_KeyDown(object sender, KeyEventArgs e)
        {
            try
            {
                if (e.KeyCode == Keys.Down)
                {
                    //While clicking down going to the listBox1 and selecting the first position
                    listBox1.Focus();
                    listBox1.SelectedIndex = 0;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void listBox1_KeyDown(object sender, KeyEventArgs e)
        {
            try
            {
                //If selected book by enter then close the listbox and just choose the one book
                if (e.KeyCode == Keys.Enter)
                {
                    textBox6.Text = listBox1.SelectedItem.ToString();
                    listBox1.Visible = false;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void listBox1_MouseClick(object sender, MouseEventArgs e)
        {
            try
            {
                //If clicked by the mouse the same efect like with enter click in listoBox1_KeyDown event
                textBox6.Text = listBox1.SelectedItem.ToString();
                listBox1.Visible = false;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                //Variables for update
                int availableAmount = 0;
                int book_id = 0;

                //Query to check if the book is available
                SqlCommand cmd2 = con.CreateCommand();
                cmd2.CommandType = CommandType.Text;
                cmd2.CommandText = "select * from book_info where name + ' - ' + author_name = '" + textBox6.Text + "'";
                cmd2.ExecuteNonQuery();
                DataTable dt2 = new DataTable();
                SqlDataAdapter da2 = new SqlDataAdapter(cmd2);
                da2.Fill(dt2);

                //Assingment of variables used later in updates
                foreach(DataRow dr2 in dt2.Rows)
                {
                    availableAmount = Convert.ToInt32(dr2["available"].ToString());
                    book_id = Convert.ToInt32(dr2["id"].ToString());
                }

                if (availableAmount > 0)
                {
                    //Insert query to the table with issuing books
                    SqlCommand cmd = con.CreateCommand();
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = "insert into issue_book (student_id,book_id,issue_date) values (" + Convert.ToInt32(textBox7.Text) + "," + book_id + ",'" + dateTimePicker1.Value.ToShortDateString() + "')";
                    cmd.ExecuteNonQuery();

                    //Update query to decrease the amount of books
                    SqlCommand cmd1 = con.CreateCommand();
                    cmd1.CommandType = CommandType.Text;
                    cmd1.CommandText = "update book_info set available = available - 1 where id = " + book_id + "";
                    cmd1.ExecuteNonQuery();

                    MessageBox.Show("Wypożyczono książkę " + textBox6.Text + " studentowi o numerze indeksu: " + textBox1.Text + "");
                }
                else
                {
                    MessageBox.Show("Książka " + textBox6.Text + " nie jest dostępna");
                }
                
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }

        }
    }
}
