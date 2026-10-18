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
    public partial class book_stock : Form
    {
        //Connection string to the local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");

        public book_stock()
        {
            InitializeComponent();
        }

        private void book_stock_Load(object sender, EventArgs e)
        {
            try
            {
                //Setting the connection
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                fill_book_info();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        public void fill_book_info()
        {
            try
            {
                //Query with list of all books
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select id as Identyfikator,name as Tytuł,author_name as Autor,publication_name as Wydawnictwo,quantity as Ilość,available as Dostępne from book_info";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                dataGridView1.DataSource = dt;
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
                //Assignment of ID of the row
                int i;
                i = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Return positions of choosen books which are borrowed
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "SELECT c.name as Imię_Nazwisko,c.index_no as Nr_indeksu,c.department as Wydział,c.phone as Telefon,c.email as Email,b.name as Tytuł,a.issue_date as Data_Wypozyczenia FROM issue_book a INNER JOIN book_info b on a.book_id = b.id INNER JOIN student_info c on a.student_id = c.id WHERE a.return_date is null and book_id = " + i + "";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                dataGridView2.DataSource = dt;
            }   
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void textBox1_KeyUp(object sender, KeyEventArgs e)
        {
            try
            {
                //Query returning list of books with the limitation to title
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select id as Identyfikator,name as Tytuł,author_name as Autor,publication_name as Wydawnictwo,quantity as Ilość,available as Dostępne from book_info where name like '%" + textBox1.Text + "%'";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                dataGridView1.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }
    }
}
