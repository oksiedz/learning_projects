/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

import java.awt.Color;
import java.io.Serializable;
import java.util.ArrayList;

/**
 *
 * @author tt
 */
public class MyPlayer implements Serializable { //class has to be serializable due to saving and loading funcionality

    private Color colour; //variable defining colour of the player
    private String name; //Name of the Player
    private int playerNum; //number of the player 1 - first, 2 - second
    private int kingX; //coordinate X of a king
    private int kingY;//coordinate Y of a king
    //Player contains also figures - so we need to have table with all figures

    public int getKingX() {
        return kingX;
    }

    public void setKingX(int kingX) {
        this.kingX = kingX;
    }

    public int getKingY() {
        return kingY;
    }

    public void setKingY(int kingY) {
        this.kingY = kingY;
    }

//container for 16 objects which is owned by the player
    //MyChessman tab[] = new MyChessman[16]; //one method
    private ArrayList<MyChessman> tab = new ArrayList<MyChessman>(); //second method

    //constructor for MyPlayer
    public MyPlayer(Color colour, String Name, int playerNum) {
        this.colour = colour;
        this.name = Name;
        this.playerNum = playerNum;

        if (playerNum == 1) {
            kingX = 4;
            kingY = 7;
        } else {
            kingX = 4;
            kingY = 0;
        }
        setKingX(kingX);
        setKingY(kingY);

        if (getPlayerNum() == 1) {
            //setting pawns
            for (int i = 0; i < 8; i++) {
                //creation of Pawns for Player
                tab.add(new MyPawn(colour, i, 6, playerNum, "Pawn " + (i + 1))); //adding Pawns in second row in each column
            }
            //setting first rook
            tab.add(new MyRook(colour, 0, 7, playerNum, "Rook 1")); //first row, position one
            tab.add(new MyRook(colour, 7, 7, playerNum, "Rook 2")); //first row, position eight
            //setting Knights
            tab.add(new MyKnight(colour, 1, 7, playerNum, "Knight 1")); //first row, position two
            tab.add(new MyKnight(colour, 6, 7, playerNum, "Knight 2"));//first row, position seven
            //setting Bishops
            tab.add(new MyBishop(colour, 2, 7, playerNum, "Bishop 1"));//first row, position three
            tab.add(new MyBishop(colour, 5, 7, playerNum, "Bishop 2"));//first row, position six
            //setting Queen
            tab.add(new MyQueen(colour, 3, 7, playerNum, "Queen"));//first row, position four
            //setting King
            tab.add(new MyKing(colour, getKingX(), getKingY(), playerNum, "King"));//first row, position five
        } else {
            //setting pawns
            for (int i = 0; i < 8; i++) {
                //creation of Pawns for Player
                tab.add(new MyPawn(colour, i, 1, playerNum, "Pawn " + (i + 1))); //adding Pawns in second row in each column
            }
            //setting first rook
            tab.add(new MyRook(colour, 0, 0, playerNum, "Rook 1"));
            tab.add(new MyRook(colour, 7, 0, playerNum, "Rook 2"));
            //setting Knights
            tab.add(new MyKnight(colour, 1, 0, playerNum, "Knight 1"));
            tab.add(new MyKnight(colour, 6, 0, playerNum, "Knight 2"));
            //setting Bishops
            tab.add(new MyBishop(colour, 2, 0, playerNum, "Bishop 1"));
            tab.add(new MyBishop(colour, 5, 0, playerNum, "Bishop 2"));
            //setting Queen
            tab.add(new MyQueen(colour, 3, 0, playerNum, "Queen"));
            //setting King
            tab.add(new MyKing(colour, getKingX(), getKingY(), playerNum, "King"));
        }

    }

    public Color getColour() {
        return colour;
    }

    public void setColour(Color colour) {
        this.colour = colour;
    }

    public String getName() {
        return name;
    }

    public void setName(String Name) {
        this.name = Name;
    }

    public ArrayList<MyChessman> getTab() {
        return tab;
    }

    public void setTab(ArrayList<MyChessman> tab) {
        this.tab = tab;
    }

    public int getPlayerNum() {
        return playerNum;
    }

    public void setPlayerNum(int playerNum) {
        this.playerNum = playerNum;
    }

}
