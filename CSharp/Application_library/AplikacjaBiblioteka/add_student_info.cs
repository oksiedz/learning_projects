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
    public partial class add_student_info : Form
    {
        //Conncetion string to the local data base
        SqlConnection con = new SqlConnection(@"Data Source=PLTOKSIEDZKI04\SQLEXPRESS;Initial Catalog=library_management_system;Integrated Security=True");
        
        //Variables used for images pwd - new file name, wantedPath - file path
        string pwd;
        string wantedPath;

        public add_student_info()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //Password generator
                pwd = Class1.GetRandomPassword(20);
                //Seting path and open image in the PictureBox
                wantedPath = Path.GetDirectoryName(Path.GetDirectoryName(System.IO.Directory.GetCurrentDirectory()));
                DialogResult result = openFileDialog1.ShowDialog();
                if (result == DialogResult.OK)
                {
                    pictureBox1.ImageLocation = openFileDialog1.FileName;
                    pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
                }
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
                //Variable for path to the image
                string imagePath;

                //Variable to check if index no is unique
                int exists = 0;

                //Coppy file to the app resoureces nad setting the path to the image
                File.Copy(openFileDialog1.FileName, wantedPath + "\\student_images\\" + pwd + ".jpg");
                imagePath = "student_images\\" + pwd + ".jpg";

                //Check on connection status if needed close and set it to be opened.
                if (con.State == ConnectionState.Open)
                {
                    con.Close();
                }
                con.Open();

                //Check if there is already student with the same index no
                SqlCommand cmd1 = con.CreateCommand();
                cmd1.CommandType = CommandType.Text;
                cmd1.CommandText = "select * from student_info where index_no ='" + textBox2.Text + "'";
                cmd1.ExecuteNonQuery();
                DataTable dt = new DataTable();
                SqlDataAdapter da = new SqlDataAdapter(cmd1);
                da.Fill(dt);
                exists = Convert.ToInt32(dt.Rows.Count.ToString());

                if (exists == 0)
                {
                    //Insertion of student data
                    SqlCommand cmd = con.CreateCommand();
                    cmd.CommandType = CommandType.Text;
                    cmd.CommandText = "insert into student_info(name,image,index_no,department,phone,email) values('" + textBox1.Text + "','" + imagePath.ToString() + "','" + textBox2.Text + "','" + textBox3.Text + "','" + textBox4.Text + "','" + textBox5.Text + "')";
                    cmd.ExecuteNonQuery();

                    MessageBox.Show("Student został dodany");
                }
                else
                {
                    MessageBox.Show("W bazie istnieje już student o numerze indeksu: " + textBox2.Text + ".");
                }

                //Setting textboxes to empty values
                textBox1.Text = "";
                textBox2.Text = "";
                textBox3.Text = "";
                textBox4.Text = "";
                textBox5.Text = "";

                //Closing the connections
                con.Close();

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
