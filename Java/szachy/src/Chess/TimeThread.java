/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author tt
 */
public class TimeThread extends Thread {

    int number;

    public TimeThread(int number) {
        this.number = number;
    }

    @Override
    public void run() {

        //code for first thread
        if (number == 1) {
            while (ChessMainFrame.gs.getSecondsplayedP1() != ChessMainFrame.gs.getGameLength()) { //calculate time since the timer for Player1 won't reach time for the game
                if (ChessMainFrame.gs.getWhoseTurn() == 1) {
                    ChessMainFrame.gs.setSecondsplayedP1(ChessMainFrame.gs.getSecondsplayedP1() + 1); //if it's Player 1 turn then add seconds
                } else {
                    ChessMainFrame.gs.setSecondsplayedP1(ChessMainFrame.gs.getSecondsplayedP1());//if it's not Player 1 turn then do not add seconds
                }
                try {
                    sleep(1000); //wait one second
                } catch (InterruptedException ex) {
                    Logger.getLogger(TimeThread.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
            if (ChessMainFrame.gs.getSecondsplayedP1() == ChessMainFrame.gs.getGameLength()) {
                ChessMainFrame.gs.setEndGame(1);
                ChessMainFrame.gs.setMate(0);
                ChessMainFrame.whoPlayes();
            }
        }
        //code for second thread
        if (number == 2) {
            while (ChessMainFrame.gs.getSecondsplayedP2() != ChessMainFrame.gs.getGameLength()) { //calculate time since the timer for Player2 won't reach time for the game
                if (ChessMainFrame.gs.getWhoseTurn() == 2) {
                    ChessMainFrame.gs.setSecondsplayedP2(ChessMainFrame.gs.getSecondsplayedP2() + 1);//if it's Player 2 turn then add seconds
                } else {
                    ChessMainFrame.gs.setSecondsplayedP2(ChessMainFrame.gs.getSecondsplayedP2());//if it's not Player 1 turn then do not add seconds
                }
                try {
                    sleep(1000);
                } catch (InterruptedException ex) {
                    Logger.getLogger(TimeThread.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
            if (ChessMainFrame.gs.getSecondsplayedP2() == ChessMainFrame.gs.getGameLength()) {
                ChessMainFrame.gs.setEndGame(1);
                ChessMainFrame.gs.setMate(0);
                ChessMainFrame.whoPlayes();
            }

        }
        if (number == 3) {
            //refreshing the remaining time
            while (ChessMainFrame.gs.getSecondsplayedP1() != ChessMainFrame.gs.getGameLength() || ChessMainFrame.gs.getSecondsplayedP2() != ChessMainFrame.gs.getGameLength()) {
                ChessMainFrame.playedPlayerTime();
                if (ChessMainFrame.gs.getEndGame() == 1) {
                    ChessMainFrame.whoWon();
                }
            }

        }
    }
}
