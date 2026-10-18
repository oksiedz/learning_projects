/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

import static Chess.ChessMainFrame.model;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JPanel;

/**
 *
 * @author ja
 */
public class MyPanel extends JPanel implements MouseListener {//mouselsitener is an abstract listener

    static MyChessman ch = null;//creating object which will contain the figure on which we clicked

    public MyPanel() {
        addMouseListener(this); //we added the Panel as a tool to listen to mouse listener
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g);

        if (ChessMainFrame.p1 != null) {
            ///painting the board
            int b; //variable to handle 1/8 of panel to paint the board
            //setting the value of b
            if (getWidth() > getHeight()) {
                b = getHeight() / 8;
            } else {
                b = getWidth() / 8;
            }
            int p = 0; //additional variable to print the colours of the board
            for (int i = 0; i < 8; i++) {
                for (int j = 0; j < 8; j++) {
                    if (p % 2 == 0) {
                        g.setColor(new Color(255, 229, 204)); //light brown
                    } else {
                        g.setColor(new Color(204, 102, 0)); //darker brown
                    }
                    g.fillRect(i * b, j * b, b, b);
                    p++;
                }
                p++;
            }

            //painting the figures for player
            g.setColor(ChessMainFrame.p1.getColour()); //setting colour from the Player
            for (int i = 0; i < ChessMainFrame.p1.getTab().size(); i++) { //i<ChessMainFrame.p1.getTab().size() - printing all figures from container of 
                ChessMainFrame.p1.getTab().get(i).drawChessman(g, b);
            }
            g.setColor(ChessMainFrame.p2.getColour()); //setting colour from the Player
            for (int i = 0; i < ChessMainFrame.p2.getTab().size(); i++) { //i<10 - printing 10 first figures
                ChessMainFrame.p2.getTab().get(i).drawChessman(g, b);
            }
        }
    }

    @Override
    public void mouseClicked(MouseEvent e) { //e - event

        if (ChessMainFrame.gs.getEndGame() != 1) {
            boolean mvNotAll = false; //variable defining if the movement is not allowed - false - movement allowed.

            //checking if the click was done on one of the figure
            int x = e.getX();
            int y = e.getY();
            //assignment of field width/height on the board
            int b; //variable to handle 1/8 of panel to paint the board
            //setting the value of b
            if (getWidth() > getHeight()) {
                b = getHeight() / 8;
            } else {
                b = getWidth() / 8;
            }
            int captured = 0;
            //index of field that we clicked
            int cx = x / b; //number of column which we have clicked
            int cy = y / b; //number of row which we have clicked
            if (ch == null) { //if we don't have marked any figure then we are checking it

                //check whose turn it is
                if (ChessMainFrame.isOccupied(cx, cy) != null) {
                    if (ChessMainFrame.gs.getWhoseTurn() == 1 && ChessMainFrame.isOccupied(cx, cy).getPlayerNum() == 1) {
                        ch = ChessMainFrame.isOccupied(cx, cy);
                    }
                    if (ChessMainFrame.gs.getWhoseTurn() == 2 && ChessMainFrame.isOccupied(cx, cy).getPlayerNum() == 2) {
                        ch = ChessMainFrame.isOccupied(cx, cy);
                    }
                }

                //check if we hit the figure
                if (ch != null) {
                }

                repaint(); //repaint the stage to check show the marked figure
            } else { //if we have already figure clicked, then in next click we have to indicate the new location of the figure
                if (cx > 7 || cy > 7 || cx < 0 || cy < 0) {
                    mvNotAll = true;
                    System.out.println("Incorrect movement.");
                } else {
                    //capture mechanism                
                    MyChessman mch = null;
                    //let's check if on the field that we want to land is already a figure which should be captured in such case
                    mch = ChessMainFrame.isOccupied(cx, cy);
                    //ch - figure which we are moving, mch - figure which is standing on the field where we want to land

                    if (mch != null && mch.getType() == "King") {
                        mvNotAll = true;
                    }

                    //Blokade that if there is Check, movement of king that it still will be check is not allowed
                    if (ch.getType() == "King") {
                        if (ch.getPlayerNum() == 1 && ChessMainFrame.isCheckWhiteKing(cx, cy)) {
                            mvNotAll = true;
                        }
                        if (ch.getPlayerNum() == 2 && ChessMainFrame.isCheckBlackKing(cx, cy)) {
                            mvNotAll = true;
                        }
                    }

                    //we can proceed only if mch is any figure - cause if there is no figure no capture is needed
                    if (mch != null && ch.IsMoveOk(cx, cy) && !mvNotAll) { //capture can be done only if move is ok.
                        //checking if marked figure and figure which is standing on target place are owned by the same player
                        if (ch.getPlayerNum() != mch.getPlayerNum()) {
                            if (mch.getPlayerNum() == 1) { //if the figure on the target field is players one then
                                ChessMainFrame.p1.getTab().remove(mch); //deleting from the container for player1 figure which is in mch - so on target field
                            } else {
                                ChessMainFrame.p2.getTab().remove(mch);
                            }
                            //adding figure to the table with captured figures
                            ChessMainFrame.model2.insertRow(ChessMainFrame.model2.getRowCount(), new Object[]{getPlayerName(mch.getPlayerNum()), mch.getType()});
                            captured = 1;
                        } else {
                            mvNotAll = true;
                        }
                    }

                    //setting mvNotAll (move not allowed to true if IsMoveOK is false - so if move is not ok (not allowed due to the movement rules) the mvNotAll should be true - saying that movement is not allowed
                    if (captured == 0 && ch.IsMoveOk(cx, cy) == false) {
                        mvNotAll = true;
                    }

                    if (!mvNotAll) { //movement is allowed
                        //moving the figure
                        //ch.setX(cx); //assigning as X cx - so new x location
                        //ch.setY(cy); //assigning as Y cy - so new y location
                        //above replace by moveChessman

                        //saving the movement to the table
                        Movement mov = new Movement(getPlayerName(ch.getPlayerNum()), ch.getType(), fieldAddress(ch.getX(), ch.getY()), fieldAddress(cx, cy));

                        ch.moveChessman(cx, cy, ch.getPlayerNum()); //moving the figure to new location

                        ChessMainFrame.model.insertRow(model.getRowCount(), new Object[]{mov.getPlayerName(), mov.getFigure(), mov.getFieldFrom(), mov.getFieldTo()});
                        if (ChessMainFrame.isCheckBlackKing(ChessMainFrame.p2.getKingX(), ChessMainFrame.p2.getKingY()) || ChessMainFrame.isCheckWhiteKing(ChessMainFrame.p1.getKingX(), ChessMainFrame.p1.getKingY())) {
                            ChessMainFrame.gs.setCheck(1);
                            ChessMainFrame.isMate();
                            ChessMainFrame.jLabelVisibitilty(1);
                            ch.setChecksKing(true);
                        } else {
                            ChessMainFrame.gs.setCheck(0);
                            ChessMainFrame.jLabelVisibitilty(0);
                            ch.setChecksKing(false);
                        }
                        ch = null; //null as ch cause now the figure won't be marked  
                        mch = null; //nulling the 
                        mov = null;

                        //setting who is playing now
                        if (ChessMainFrame.gs.getWhoseTurn() == 1) {
                            ChessMainFrame.gs.setWhoseTurn(2);
                        } else {
                            ChessMainFrame.gs.setWhoseTurn(1);
                        }
                    } else { //movement is not allowed
                        System.out.println("Movement not allowed.");
                        ch = null; //remarking the figure
                        mch = null; //reselecting the target figure
                    }
                    //refreshing the label
                    ChessMainFrame.whoPlayes();

                    repaint(); //refresh the board
                }
            }
        }

    }

    @Override
    public void mousePressed(MouseEvent e) {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void mouseEntered(MouseEvent e) {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void mouseExited(MouseEvent e) {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    private String fieldAddress(int a, int b) {
        String fieldAddress = "";
        switch (a) {
            case 0 ->
                fieldAddress = "A";
            case 1 ->
                fieldAddress = "B";
            case 2 ->
                fieldAddress = "C";
            case 3 ->
                fieldAddress = "D";
            case 4 ->
                fieldAddress = "E";
            case 5 ->
                fieldAddress = "F";
            case 6 ->
                fieldAddress = "G";
            case 7 ->
                fieldAddress = "H";
        };
        switch (b) {
            case 0 ->
                fieldAddress = fieldAddress + "8";
            case 1 ->
                fieldAddress = fieldAddress + "7";
            case 2 ->
                fieldAddress = fieldAddress + "6";
            case 3 ->
                fieldAddress = fieldAddress + "5";
            case 4 ->
                fieldAddress = fieldAddress + "4";
            case 5 ->
                fieldAddress = fieldAddress + "3";
            case 6 ->
                fieldAddress = fieldAddress + "2";
            case 7 ->
                fieldAddress = fieldAddress + "1";
        };
        return fieldAddress;
    }

    private String getPlayerName(int playerNum) {
        if (playerNum == 1) {
            return ChessMainFrame.p1.getName();
        } else {
            return ChessMainFrame.p2.getName();
        }
    }
}
