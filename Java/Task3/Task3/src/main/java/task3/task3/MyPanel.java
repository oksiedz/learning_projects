/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package task3.task3;

import java.awt.Graphics;
import static java.lang.Math.min;
import javax.swing.JPanel;

/**
 *
 * @author tt
 */
public class MyPanel extends JPanel {

    int ax1;
    int ay1;
    int ax2;
    int ay2;
    int ax3;
    int ay3;
    int ax4;
    int ay4;

    public void setParams(int ax1, int ay1, int ax2, int ay2, int ax3, int ay3, int ax4, int ay4) {
        this.ax1 = ax1;
        this.ay1 = ay1;
        this.ax2 = ax2;
        this.ay2 = ay2;
        this.ax3 = ax3;
        this.ay3 = ay3;
        this.ax4 = ax4;
        this.ay4 = ay4;
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g); //To change body of generated methods, choose Tools | Templates.

        //Cartesian drawing
        double MyPanelWidth = getWidth();
        double MyPanelHeight = getHeight();
        //drawing lines OX and OY
        g.drawLine((int) (MyPanelWidth / 2), 0, (int) (MyPanelWidth / 2), (int) MyPanelHeight);
        g.drawLine(0, (int) (MyPanelHeight / 2), (int) MyPanelWidth, (int) (MyPanelHeight / 2));
        //drawing arrows
        g.drawLine((int) (MyPanelWidth / 2), 0, (int) (MyPanelWidth / 2 + 5), 10);
        g.drawLine((int) (MyPanelWidth / 2), 0, (int) (MyPanelWidth / 2 - 5), 10);
        g.drawLine((int) (MyPanelWidth), (int) (MyPanelHeight / 2), (int) (MyPanelWidth - 10), (int) (MyPanelHeight / 2) - 5);
        g.drawLine((int) (MyPanelWidth), (int) (MyPanelHeight / 2), (int) (MyPanelWidth - 10), (int) (MyPanelHeight / 2) + 5);

        float ratioH = (float) ((float) (MyPanelHeight / 2) / 284.5);
        float ratioW = (float) ((float) (MyPanelWidth / 2) / 344);

        //Centralizing trapezoid
        int new_ax1 = (int) (ax1 * ratioW + MyPanelWidth / 2);
        int new_ax2 = (int) (ax2 * ratioW + MyPanelWidth / 2);
        int new_ax3 = (int) (ax3 * ratioW + MyPanelWidth / 2);
        int new_ax4 = (int) (ax4 * ratioW + MyPanelWidth / 2);
        int new_ay1 = (int) (MyPanelHeight / 2 - ay1 * ratioH);
        int new_ay2 = (int) (MyPanelHeight / 2 - ay2 * ratioH);
        int new_ay3 = (int) (MyPanelHeight / 2 - ay3 * ratioH);
        int new_ay4 = (int) (MyPanelHeight / 2 - ay4 * ratioH);

        int x[] = {new_ax1, new_ax2, new_ax3, new_ax4};

        int y[] = {new_ay1, new_ay2, new_ay3, new_ay4};

        int noofpoints = x.length;
        g.drawPolygon(x, y, noofpoints);

    }

}
