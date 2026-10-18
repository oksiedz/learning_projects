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
public class MyPawn extends MyChessman implements Serializable {

    private boolean moved = false;

    public MyPawn(Color color, int x, int y, int playerNum, String type) {
        super(color, x, y, playerNum, type); //constructor from Parent Class MyChessman
    }

    public boolean isMoved() {
        return moved;
    }

    public void setMoved(boolean moved) {
        this.moved = moved;
    }

    @Override
    public boolean IsMoveOk(int a, int b) {
        //System.out.println("Test0");
        if (a == getX()) {//if the pawn is moving on the vertical line
            if (!moved) {//if pawn was not moved then it can move 1 or 2 fields
                if (getPlayerNum() == 1) {
                    //System.out.println("Test1");
                    return ((getY() - b == 1 || getY() - b == 2) && ChessMainFrame.isOccupied(a, b) == null);//true if difference is 1 or 2
                } else {
                    //System.out.println("Test2");
                    return ((b - getY() == 1 || b - getY() == 2)) && ChessMainFrame.isOccupied(a, b) == null;//true if difference is 1 or 2
                }
            } else {//if it was moved then only one field up/down
                if (getPlayerNum() == 1) {
                    //System.out.println("Test3");
                    return ((getY() - b == 1) && ChessMainFrame.isOccupied(a, b) == null);//true if difference is 1
                } else {
                    //System.out.println("Test4");
                    return ((b - getY() == 1) && ChessMainFrame.isOccupied(a, b) == null);//true if difference is 1
                }
            }
        } else {//if pawn is changing the vertical line
            if ((a - getX() == -1 && getPlayerNum() == 1 && b - getY() == -1 && ChessMainFrame.isOccupied(a, b) != null)
                    || (a - getX() == -1 && getPlayerNum() == 2 && b - getY() == 1 && ChessMainFrame.isOccupied(a, b) != null)
                    || (a - getX() == 1 && getPlayerNum() == 1 && b - getY() == -1 && ChessMainFrame.isOccupied(a, b) != null)
                    || (a - getX() == 1 && getPlayerNum() == 2 && b - getY() == 1 && ChessMainFrame.isOccupied(a, b) != null)) {
                //System.out.println("Test5");
                return true;
            } else {
                //System.out.println("Test6");
                return false;
            }
        }

    }
    //Class for Pawn

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
            g2.setStroke(new BasicStroke(8)); //setiing the width of the oval which we draw
            g.drawOval(getX() * b, getY() * b, b, b); //draving oval around the figure which was clicked
        }

    }

    @Override
    public void moveChessman(int a, int b, int playerNo) {
        setX(a);
        setY(b);
        setMoved(true);

    }
}
