/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Chess;

/**
 *
 * @author tt
 */
public class Movement {

    private String playerName;
    private String figure;
    private String fieldFrom;
    private String fieldTo;

    public Movement(String playerName, String figure, String fieldFrom, String fieldTo) {
        this.playerName = playerName;
        this.figure = figure;
        this.fieldFrom = fieldFrom;
        this.fieldTo = fieldTo;
    }

    public String getFieldTo() {
        return fieldTo;
    }

    public void setFieldTo(String fieldTo) {
        this.fieldTo = fieldTo;
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public String getFigure() {
        return figure;
    }

    public void setFigure(String figure) {
        this.figure = figure;
    }

    public String getFieldFrom() {
        return fieldFrom;
    }

    public void setFieldFrom(String fieldFrom) {
        this.fieldFrom = fieldFrom;
    }

}
