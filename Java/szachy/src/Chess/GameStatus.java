/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

import java.io.Serializable;

/**
 *
 * @author tt
 */
public class GameStatus implements Serializable {

    private int whoseTurn = 1;
    private int check = 0;
    private int mate = 0;
    private int endGame = 0;
    private int gameLength = 3600;
    private int secondsplayedP1 = 0;
    private int secondsplayedP2 = 0;
    private int winner;

    public int getWhoseTurn() {
        return whoseTurn;
    }

    public void setWhoseTurn(int whoseTurn) {
        this.whoseTurn = whoseTurn;
    }

    public int getCheck() {
        return check;
    }

    public void setCheck(int check) {
        this.check = check;
    }

    public int getMate() {
        return mate;
    }

    public void setMate(int mate) {
        this.mate = mate;
    }

    public int getEndGame() {
        return endGame;
    }

    public void setEndGame(int endGame) {
        this.endGame = endGame;
    }

    public int getGameLength() {
        return gameLength;
    }

    public void setGameLength(int gameLength) {
        this.gameLength = gameLength;
    }

    public int getSecondsplayedP1() {
        return secondsplayedP1;
    }

    public void setSecondsplayedP1(int secondsplayedP1) {
        this.secondsplayedP1 = secondsplayedP1;
    }

    public int getSecondsplayedP2() {
        return secondsplayedP2;
    }

    public void setSecondsplayedP2(int secondsplayedP2) {
        this.secondsplayedP2 = secondsplayedP2;
    }

    public int getWinner() {
        return winner;
    }

    public void setWinner(int winner) {
        this.winner = winner;
    }

}
