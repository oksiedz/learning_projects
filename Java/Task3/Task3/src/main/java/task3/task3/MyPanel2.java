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
public class MyPanel2 extends JPanel {

    int[] X = new int[9999999];
    int[] Y = new int[9999999];
    int iterator = 0;

    public void setParams(int iterator, int[] Xinput, int[] Yinput) {
        this.iterator = iterator;
        this.X = Xinput;
        this.Y = Yinput;
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

        float ratioW2 = (float) ((float) ((MyPanelWidth) / 2) / 348.5);
        float ratioH2 = (float) ((float) (MyPanelHeight / 2) / 348.5);
        //Centralizing trapezoid
        if (iterator != 0) {
            int[] Xmod = new int[iterator + 1];
            int[] Ymod = new int[iterator + 1];

            for (int i = 0; i < iterator; i++) {
                Xmod[i] = (int) (X[i] * ratioW2 + MyPanelWidth / 2);
                Ymod[i] = (int) (MyPanelHeight / 2 - Y[i] * ratioH2);
            }

            Xmod[iterator] = Xmod[0];
            Ymod[iterator] = Ymod[0];

            g.drawPolygon(Xmod, Ymod, iterator + 1);
        }

    }

}
