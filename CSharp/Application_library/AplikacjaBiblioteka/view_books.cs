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
    public partial class view_books : Form
    {
        //Connection string to the local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");
        public view_books()
        {
            InitializeComponent();
        }

        private void view_books_Load(object sender, EventArgs e)
        {
            //Present the list of books
            disp_books();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //Variable for search category
                string category = "";
                
                //Variable for data count
                int i = 0;
                
                //Set the searching column depending on the choosen value from comboBox
                switch (comboBox1.Text)
                {
                    case "Tytuł":
                        category = "name";
                        break;
                    case "Autor":
                        category = "author_name";
                        break;
                    case "Wydawnictwo":
                        category = "publication_name";
                        break;
                    default:
                        category = "";
                        break;
                }

                //Check the connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Select query
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                if (category == "")
                {
                    cmd.CommandText = "select Id as Identyfikator, name as Tytuł, author_name as Autor, publication_name as Wydawnictwo, purchase_date as Data_zakupu, quantity as Ilość, available as Dostępne from book_info";
                }
                else
                {
                    cmd.CommandText = "select id as Identyfikator, name as Tytuł, author_name as Autor, publication_name as Wydawnictwo, purchase_date as Data_zakupu, quantity as Ilość, available as Dostępne from book_info where " + category + " like '%" + textBox2.Text + "%'";
                }
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                i = Convert.ToInt32(dt.Rows.Count.ToString());
                dataGridView1.DataSource = dt;

                //Closing the connection
                con.Close();

                if (i == 0)
                {
                    MessageBox.Show("Nie ma pozycji spełniających kryteria wyszukiwania.");
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                //Panel will be visible only if user click on the data grid
                panel2.Visible = true;

                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Checking the connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Select query for books info
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select id as Identyfikator, name as Tytuł, author_name as Autor, publication_name as Wydawnictwo, purchase_date as Data_zakupu, quantity as Ilość, available as Dostępne from book_info where id = " + i + "";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                
                //Presentation of row data into boxes
                foreach(DataRow dr in dt.Rows)
                {
                    textBox1.Text = dr["Tytuł"].ToString();
                    textBox3.Text = dr["Autor"].ToString();
                    textBox4.Text = dr["Wydawnictwo"].ToString();
                    dateTimePicker1.Value = Convert.ToDateTime(dr["Data_Zakupu"].ToString());
                    textBox6.Text = dr["Ilość"].ToString();
                }    

                //Closing the connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Check the connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Update query to edit the data
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "update book_info set name = '" + textBox1.Text + "', author_name = '" + textBox3.Text + "', publication_name='" + textBox4.Text  + "', purchase_date = '" + DateTime.Parse(dateTimePicker1.Text) + "', quantity ='" + textBox6.Text + "' where id = " + i +"";
                cmd.ExecuteNonQuery();

                //Present the list of books
                disp_books();
                
                //Hide the panel with edit data
                panel2.Visible = false;
                
                MessageBox.Show("Pozycja zaktualizowana");

                //Closing the connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        public void disp_books()
        {
            try
            {
                //Checking connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Select query for book info
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select Id as Identyfikator, name as Tytuł, author_name as Autor, publication_name as Wydawnictwo, purchase_date as Data_zakupu, quantity as Ilość, available as Dostępne from book_info";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                dataGridView1.DataSource = dt;

                //Closing the connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            try
            {
                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Checking the connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Delete query
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "delete from book_info where id = " + i + "";
                cmd.ExecuteNonQuery();

                //Present the list of books
                disp_books();

                //Hide the panel with edit data
                panel2.Visible = false;
                
                MessageBox.Show("Pozycja usunięta");

                //Closing the connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
