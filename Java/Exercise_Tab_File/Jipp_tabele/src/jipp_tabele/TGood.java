/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package jipp_tabele;

/**
 *
 * @author tt
 */
public class TGood extends TValue{
    
    private int sizeX;
    private int sizeY;
    private int sizeZ;

    public TGood(int sizeX, int sizeY, int sizeZ) {
        this.sizeX = sizeX;
        this.sizeY = sizeY;
        this.sizeZ = sizeZ;
    }


    @Override
    public String getDescription() {
        return "("+sizeX + ", "+sizeY+", "+sizeZ + ") : pojemnosc = " + (sizeX*sizeY*sizeZ);
    }

    public int getSizeX() {
        return sizeX;
    }

    public void setSizeX(int sizeX) {
        this.sizeX = sizeX;
    }

    public int getSizeY() {
        return sizeY;
    }

    public void setSizeY(int sizeY) {
        this.sizeY = sizeY;
    }

    public int getSizeZ() {
        return sizeZ;
    }

    public void setSizeZ(int sizeZ) {
        this.sizeZ = sizeZ;
    }
}
