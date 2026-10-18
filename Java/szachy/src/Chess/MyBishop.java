/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.io.Serializable;
import static java.lang.Math.abs;

/**
 *
 * @author tt
 */
public class MyBishop extends MyChessman implements Serializable {
//Class for Bishop figure

    public MyBishop(Color colour, int x, int y, int playerNum, String type) {
        super(colour, x, y, playerNum, type);
    }

    @Override
    public boolean IsMoveOk(int a, int b) {
        //System.out.println("a=" + a + ";getX=" + getX() + ";b=" + b + ";getY=" + getY());
        if (a == getX() || b == getY()) { //bishop is moving on diagonal so if one of the coordinates didn't change then it's incorrect movement
            return false;
        } else {
            if (abs(a - getX()) != abs(b - getY())) { //the movement is on diagonal, so the change of X and Y is of the same size cannot change 2 in X and 3 in Y
                return false;
            } else { //here there is already diagonal movement but there is to be considered movement till the next figure
                //technical variables
                int ile; //for X
                int ile2;//for Y
                int k;//for X
                int k2;//for Y
                MyChessman f = null; //variable on which there will be saved the figure
                //bishop goes on the right diagonal
                if (a - getX() > 0) {
                    ile = 1;
                } else { //bishop goes on the left diagonal
                    ile = -1;
                }
                if (b - getY() > 0) {//bishop goes down diagonal
                    ile2 = 1;
                } else { //bishop goes up diagonal
                    ile2 = -1;
                }
                k = getX() + ile;
                k2 = getY() + ile2;
                //System.out.println("ile=" + ile + ";ile2=" + ile2 + ";k=" + k + ";k2=" + k2);
                //System.out.println("Start a=" + a + ";k=" + k);
                while (k != a && k >= 0 && k <= 8 && k2 >= 0 && k2 <= 8) {
                    //System.out.println("k=" + k + ";k2=" + k2);
                    f = ChessMainFrame.isOccupied(k, k2);
                    if (f != null) {
                        return false;
                    }
                    k = k + ile;
                    k2 = k2 + ile2;
                    //System.out.println("k=" + k + ";a=" + a + ";k2=" + k2);
                }
                return true;
            }
        }
    }

    @Override
    public void drawChessman(Graphics g, int b) {
        g.setColor(getColour());//setting the colour to the Player's colour
        g.fillOval(getX() * b, getY() * b, b, b); //drawing oval shape as a figure
        //setting the colour to the opposite colour to the Player's colour
        if (getPlayerNum() == 1) {
            g.setColor(Color.BLACK);
        } else {
            g.setColor(Color.WHITE);
        }
        //drawing name of the figure
        g.drawString(getType(), getX() * b + b / 3, getY() * b + b / 2);
        //if the figure was clicked then it should be marked with new circle colour (this == ch from MyPanel
        if (this == MyPanel.ch) {
            g.setColor(Color.GREEN); //changing colour to green
            Graphics2D g2 = (Graphics2D) g;//conversion to Graphics2D to set stroke
            g2.setStroke(new BasicStroke(8));//setiing the width of the oval which we draw
            g.drawOval(getX() * b, getY() * b, b, b); //draving oval around the figure which was clicked
        }
    }

    @Override
    public void moveChessman(int a, int b, int playerNo) {
        setX(a);
        setY(b);
    }

}
