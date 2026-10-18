/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package watki;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author tt
 */
public class MyFred extends Thread{
    
    int numer;
static int koniec = 0;
int ile = 0;
    public MyFred(int numer) {
        this.numer = numer;
    }
    
    @Override
    public void run()
    {
        while(true)
        {
            try {
                System.out.println("Czesc jestem watkiem : "+ numer + " ile: " + ile);
                koniec++;
                ile++;
                
                sleep(1000*numer);
                
                
                if(koniec > 100)
                    break;
            } catch (InterruptedException ex) {
                Logger.getLogger(MyFred.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
