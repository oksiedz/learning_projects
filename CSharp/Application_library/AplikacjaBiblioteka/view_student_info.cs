using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Data.SqlClient;

namespace AplikacjaBiblioteka
{
    public partial class view_student_info : Form
    {
        //Connection string to local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");
        
        //Variables for filename and path and creation of dialog result
        string pwd;
        string wantedPath;
        DialogResult result;
        
        public view_student_info()
        {
            InitializeComponent();
        }

        private void view_student_info_Load(object sender, EventArgs e)
        {
            try
            {
                //Connection check
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Filling grid with data
                fill_grid();

                //Closing connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        public void fill_grid()
        {
            try
            {
                //Clearing data in the grid
                dataGridView1.Columns.Clear();
                dataGridView1.Refresh();
                
                //Local variable for iteration
                int j = 0;

                //Select query for student info
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select Id as Identyfikator, name as Imie_Nazwisko, index_no as Nr_Indeksu, department as Wydział, phone as Telefon, email as EMail, image as Zdjęcie from student_info";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                dataGridView1.DataSource = dt;

                //Preview of picture
                Bitmap img;
                DataGridViewImageColumn imageCol = new DataGridViewImageColumn();
                imageCol.Width = 500;
                imageCol.HeaderText = "Podgląd zdjęcia";
                imageCol.ImageLayout = DataGridViewImageCellLayout.Zoom;
                imageCol.Width = 100;
                dataGridView1.Columns.Add(imageCol);

                //Adding preview of picture to each row of the table
                foreach (DataRow dr in dt.Rows)
                {
                    img = new Bitmap(@"..\..\" + dr["Zdjęcie"].ToString());
                    dataGridView1.Rows[j].Cells[7].Value = img;
                    dataGridView1.Rows[j].Height = 100;
                    j = j + 1;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void textBox1_KeyUp(object sender, KeyEventArgs e)
        {
            try
            {
                //Local variable for iterations
                int j = 0;
                
                //Refreshing the grid view
                dataGridView1.Columns.Clear();
                dataGridView1.Refresh();

                //Checking connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Select query for students data
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select Id as Identyfikator, name as Imie_Nazwisko, index_no as Nr_Indeksu, department as Wydział, phone as Telefon, email as EMail, image as Zdjęcie from student_info where name like '%" + textBox1.Text + "%' or index_no like '%" + textBox1.Text + "%' or department like '%" + textBox1.Text + "%' or phone like '%" + textBox1.Text + "%' or email like '%" + textBox1.Text + "%'";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);

                int rowCount = Convert.ToInt32(dt.Rows.Count.ToString());
                
                dataGridView1.DataSource = dt;

                //Preview of the photo
                Bitmap img;
                DataGridViewImageColumn imageCol = new DataGridViewImageColumn();
                imageCol.Width = 500;
                imageCol.HeaderText = "Podgląd zdjęcia";
                imageCol.ImageLayout = DataGridViewImageCellLayout.Zoom;
                imageCol.Width = 100;
                dataGridView1.Columns.Add(imageCol);

                //Adding photo preview to each row
                foreach (DataRow dr in dt.Rows)
                {
                    img = new Bitmap(@"..\..\" + dr["Zdjęcie"].ToString());
                    dataGridView1.Rows[j].Cells[7].Value = img;
                    dataGridView1.Rows[j].Height = 100;
                    j = j + 1;
                }

                if (rowCount == 0)
                {
                    MessageBox.Show("Nie ma pozycji spełniających kryteria wyszukiwania.");
                }
                
                //Closing connection
                con.Close();
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
                //Checking connection status
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //ID of the student
                int id;
                id = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                //Select Query for particular student (selected)
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = "select * from student_info where id = '" + id + "'";
                cmd.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);

                //Presentation of student data in particular boxes
                foreach (DataRow dr in dt.Rows)
                {
                    textBox2.Text = dr["name"].ToString();
                    textBox3.Text = dr["index_no"].ToString();
                    textBox4.Text = dr["department"].ToString();
                    textBox5.Text = dr["phone"].ToString();
                    textBox6.Text = dr["email"].ToString();
                }

                //Connection close
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //Password generator - file name
                pwd = Class1.GetRandomPassword(20);
                wantedPath = Path.GetDirectoryName(Path.GetDirectoryName(System.IO.Directory.GetCurrentDirectory()));
                result = openFileDialog1.ShowDialog();
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
                //Checking the status of the connection
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();
                
                //If depending of the result of choosen photo - ok if it was choosen, cancel if not opened photo
                if (result == DialogResult.OK)
                {
                    //Variable for id of selected cell
                    int id;
                    id = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                    //Path of the photo file
                    string imagePath;
                    File.Copy(openFileDialog1.FileName, wantedPath + "\\student_images\\" + pwd + ".jpg");
                    imagePath = "student_images\\" + pwd + ".jpg";

                    //Update query with photo
                    SqlCommand cmd = con.CreateCommand();
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = "update student_info set name = '" + textBox2.Text + "', image = '" + imagePath.ToString() + "', index_no = '" + textBox3.Text + "', department = '" + textBox4.Text + "', phone = '" + textBox5.Text + "', email = '" + textBox6.Text + "' where id = '" + id + "'";
                    cmd.ExecuteNonQuery();
                    
                    //Update the presented rows
                    fill_grid();

                    MessageBox.Show("Zaktualizowno dane");
                }
                else if (result == DialogResult.Cancel)
                {
                    //Variable for id of selected cell
                    int id;
                    id = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());

                    //Update query with photo
                    SqlCommand cmd = con.CreateCommand();
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = "update student_info set name = '" + textBox2.Text + "', index_no = '" + textBox3.Text + "', department = '" + textBox4.Text + "', phone = '" + textBox5.Text + "', email = '" + textBox6.Text + "' where id = '" + id + "'";
                    cmd.ExecuteNonQuery();

                    //Update the presented rows
                    fill_grid();

                    MessageBox.Show("Zaktualizowno dane");
                }

                //Close the connection
                con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message.ToString());
            }
        }
    }
}
