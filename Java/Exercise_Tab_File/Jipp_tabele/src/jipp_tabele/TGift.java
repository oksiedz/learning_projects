/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package jipp_tabele;

/**
 *
 * @author tt
 */
public class TGift extends TValue{
    private String giftName;
    private double prize;
    private String ForWho;
    private int weight;

    public TGift(String giftName, double prize, String ForWho, int weight) {
        this.giftName = giftName;
        this.prize = prize;
        this.ForWho = ForWho;
        this.weight = weight;
    }

    public String getGiftName() {
        return giftName;
    }

    public void setGiftName(String giftName) {
        this.giftName = giftName;
    }

    public double getPrize() {
        return prize;
    }

    public void setPrize(double prize) {
        this.prize = prize;
    }

    public String getForWho() {
        return ForWho;
    }

    public void setForWho(String ForWho) {
        this.ForWho = ForWho;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    @Override
    public String toString() {
        return "TGift{" + "giftName=" + giftName + ", prize=" + prize + ", ForWho=" + ForWho + ", weight=" + weight + '}';
    }

    @Override
    public String getDescription() {
return this.toString();    }
    
    
}
