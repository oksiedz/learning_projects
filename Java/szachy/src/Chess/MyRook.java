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

/**
 *
 * @author tt
 */
public class MyRook extends MyChessman implements Serializable {
//class for Tower figure

    public MyRook(Color colour, int x, int y, int playerNum, String type) {
        super(colour, x, y, playerNum, type);
    }

    @Override
    public boolean IsMoveOk(int a, int b) {
        //we can move as far as there is figure (if it's different player then we can capture the field)
        int ile = 1; //1 if we are going down or right, -1 when we are going up or left
        int k = -1; //additonal variable useful for while
        //if we change both locations then it's incorrect movement
        if (a != getX() && b != getY()) {
            return false;
        } else { //other cases that we are chaning one coordinate
            if (a != getX()) { //if we are chainng coordinate X - we can move so far when there is another figure
                MyChessman f = null;
                if (getX() > a) {//if we are considering move in the left direction
                    ile = -1;
                }
                k = getX() + ile; //X assigned to k
                while (k != a) {//we are moving to the last field before target one - we are going from getX to a direction
                    //we need to check if there are any figures   
                    f = ChessMainFrame.isOccupied(k, b); //if on the next field there is figure
                    if (f != null) {
                        return false;
                    }
                    k = k + ile;
                }
            }
            if (b != getY()) { //if we are chainng coordinate X - we can move so far when there is another figure
                MyChessman f = null;
                if (getY() > b) {//if we are considering move in the up direction
                    ile = -1;
                }
                k = getY() + ile; //X assigned to k
                while (k != b) {//we are moving to the last field before target one - we are going from getX to a direction
                    //we need to check if there are any figures   
                    f = ChessMainFrame.isOccupied(a, k); //if on the next field there is figure
                    if (f != null) {
                        return false;
                    }
                    k = k + ile;
                }
            }
            return true;
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
        //if the figure was clicked then it should be marked with new circle colour (this == ch from MyPanel
        if (this == MyPanel.ch) {
            g.setColor(Color.GREEN); //changing colour to green
            Graphics2D g2 = (Graphics2D) g;//conversion to Graphics2D to set stroke
            g2.setStroke(new BasicStroke(8)); //setiing the width of the oval which we draw
            g.drawOval(getX() * b, getY() * b, b, b); //draving oval around the figure which was clicked
        }
    }

    @Override
    public void moveChessman(int a, int b, int playerNo) {
        setX(a);
        setY(b);
    }

}
