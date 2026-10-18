using System;
using System.Data;
using System.Configuration;
using System.Web;

public class Class1
{
	
        public static string GetRandomPassword(int length)
        {
            //Array of chars
            char[] chars = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ".ToCharArray();
            //Creation of empty sting for password (name of file)
            string password = string.Empty;
            //New instance of random
            Random random = new Random();

            //Creation of file name by loop for defined length
            for (int i = 0; i < length; i++)
            {
                //Value of char
                int x = random.Next(1, chars.Length);
                //For avoiding Repetation of Characters
                if (!password.Contains(chars.GetValue(x).ToString()))
                {
                    password += chars.GetValue(x);
                }
                else
                {
                    i = i - 1;
                }
            }
            return password;
        }

}
