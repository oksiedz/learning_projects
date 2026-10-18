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
    public partial class return_book : Form
    {
        //Connection string to the local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");

        public return_book()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //Fill the grid with results
                fill_grid(textBox1.Text);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void return_book_Load(object sender, EventArgs e)
        {
            try
            {
                {
                    //Setting the connection
                    if (con.State == ConnectionState.Open)
                    {
                        con.Close();
                    }
                    con.Open();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        public void fill_grid(string index_no)
        {
            try
            {
                //Variable to check if there are data
                int count = 0;

                //Query for all issued books
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "SELECT a.id,b.id as Student_id,b.name as Student_Imię_Nazwisko,b.index_no as Nr_indeksu,b.department as Wydział,b.phone as Telefon,b.email as Email,c.id as Książka_id,c.name as Tytuł,c.author_name as Autor, a.issue_date as Data_Wypożyczenia FROM issue_book a INNER JOIN student_info b ON a.student_id = b.Id INNER JOIN book_info c ON a.book_id = c.Id WHERE a.return_date is null and b.index_no = '" + index_no.ToString() + "'";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);

                count = Convert.ToInt32(dt.Rows.Count.ToString());

                if (count > 0)
                {
                    //Fill the grid with data results
                    dataGridView1.DataSource = dt;
                    
                    //Show panel 2
                    panel2.Visible = true;
                }
                else
                {
                    MessageBox.Show("Student nie ma aktywnych wypożyczeń.");
                }    
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                //Show panel 3
                panel3.Visible = true;
                
                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Query for all issued books
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "SELECT a.id,b.id as Student_id,b.name as Student_Imię_Nazwisko,b.index_no as Nr_indeksu,b.department as Wydział,b.phone as Telefon,b.email as Email,c.id as Książka_id,c.name as Tytuł,c.author_name as Autor, a.issue_date as Data_Wypożyczenia FROM issue_book a INNER JOIN student_info b ON a.student_id = b.Id INNER JOIN book_info c ON a.book_id = c.Id WHERE a.id =" + i + "";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);

                //Show as labels title and issue date
                foreach(DataRow dr in dt.Rows)
                {
                    label3.Text = dr["Tytuł"].ToString();
                    label5.Text = dr["Data_Wypożyczenia"].ToString();
                }
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
                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Update return date
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "update issue_book set return_date = '" + dateTimePicker1.Value.ToString() + "' where id = " + i + "";
                cmd.ExecuteNonQuery();

                //Update available quantity
                SqlCommand cmd1 = con.CreateCommand();
                cmd1.CommandType = CommandType.Text;
                cmd1.CommandText = "update a set a.available = a.available + 1 from book_info a INNER JOIN issue_book b on a.id = b.book_id where b.id = " + i + "";
                cmd1.ExecuteNonQuery();

                MessageBox.Show("Książka zwrócona.");

                //Hide panels
                panel2.Visible = false;
                panel3.Visible = false;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }
    }
}
