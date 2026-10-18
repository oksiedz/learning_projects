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
public class Animator extends Thread{
    
    MyPanel p;

    public Animator(MyPanel p) {
        this.p = p;
    }
    
    @Override
    public void run()
    {
        while (true) {            
            MyPanel.x++;
            MyPanel.y++;
            p.repaint();
            try {
                sleep(250);
            } catch (InterruptedException ex) {
                Logger.getLogger(Animator.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
