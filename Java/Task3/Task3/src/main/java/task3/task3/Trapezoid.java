/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package task3.task3;

import static java.lang.Math.abs;

/**
 *
 * @author tt
 */
public class Trapezoid {

    private int x1;
    private int y1;
    private int x2;
    private int y2;
    private int x3;
    private int y3;
    private int x4;
    private int y4;
    private float slope1;
    private float slope2;
    private float slope3;
    private float slope4;
    private float circuit;
    private float area;

    public float getCircuit() {
        return circuit;
    }

    private void setCircuit() {
        this.circuit = calculateCircuitOfTrapeze();
    }

    public float getArea() {
        return area;
    }

    private void setArea() {
        this.area = calcualteAreaOfTrapeze();
    }

    public Trapezoid(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
        this.x3 = x3;
        this.y3 = y3;
        this.x4 = x4;
        this.y4 = y4;

        setSlope1();
        setSlope2();
        setSlope3();
        setSlope4();
        setCircuit();
        setArea();

    }

    public int getX1() {
        return x1;
    }

    public void setX1(int x1) {
        this.x1 = x1;
    }

    public int getY1() {
        return y1;
    }

    public void setY1(int y1) {
        this.y1 = y1;
    }

    public int getX2() {
        return x2;
    }

    public void setX2(int x2) {
        this.x2 = x2;
    }

    public int getY2() {
        return y2;
    }

    public void setY2(int y2) {
        this.y2 = y2;
    }

    public int getX3() {
        return x3;
    }

    public void setX3(int x3) {
        this.x3 = x3;
    }

    public int getY3() {
        return y3;
    }

    public void setY3(int y3) {
        this.y3 = y3;
    }

    public int getX4() {
        return x4;
    }

    public void setX4(int x4) {
        this.x4 = x4;
    }

    public int getY4() {
        return y4;
    }

    public void setY4(int y4) {
        this.y4 = y4;
    }

    private float CalcualteSlope(int x1, int y1, int x2, int y2) {
        return abs(((float) y2 - (float) y1) / ((float) x2 - (float) x1));
    }

    public float getSlope1() {
        return slope1;
    }

    public void setSlope1() {
        this.slope1 = CalcualteSlope(getX1(), getY1(), getX2(), getY2());
    }

    public float getSlope2() {
        return slope2;
    }

    public void setSlope2() {
        this.slope2 = CalcualteSlope(getX2(), getY2(), getX3(), getY2());
    }

    public float getSlope3() {
        return slope3;
    }

    public void setSlope3() {
        this.slope3 = CalcualteSlope(getX3(), getY3(), getX4(), getY4());
    }

    public float getSlope4() {
        return slope4;
    }

    public void setSlope4() {
        this.slope4 = CalcualteSlope(getX4(), getY4(), getX1(), getY1());
    }

    public int isTrapeze() {
        if (getSlope1() == getSlope3() || getSlope2() == getSlope4()) {
            return 1;

        } else {
            return 0;
        }
    }

    private float calculateDistanceBetweenPoints(
            int x1,
            int y1,
            int x2,
            int y2) {
        return (float) Math.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1));
    }

    private float calculateCircuitOfTrapeze() {
        return calculateDistanceBetweenPoints(getX1(), getY1(), getX2(), getY2())
                + calculateDistanceBetweenPoints(getX2(), getY2(), getX3(), getY3())
                + calculateDistanceBetweenPoints(getX3(), getY3(), getX4(), getY4())
                + calculateDistanceBetweenPoints(getX4(), getY4(), getX1(), getY1());
    }

    private float calcualteAreaOfTrapeze() {
        float distanceBase1;
        float distanceBase2;
        float height;

        if (getSlope1() == getSlope3()) {
            distanceBase1 = calculateDistanceBetweenPoints(getX1(), getY1(), getX2(), getY2());
            distanceBase2 = calculateDistanceBetweenPoints(getX3(), getY3(), getX4(), getY4());
            height = findHeightOfTrapeze(getX4(), getY4(), getX1(), getY1(), getX2(), getY2());
        } else {
            distanceBase1 = calculateDistanceBetweenPoints(getX2(), getY2(), getX3(), getY3());
            distanceBase2 = calculateDistanceBetweenPoints(getX4(), getY4(), getX1(), getY1());
            height = findHeightOfTrapeze(getX4(), getY4(), getX2(), getY2(), getX3(), getY3());
        }

        return (distanceBase1 + distanceBase2) * height / 2;
    }

    static float findHeightOfTrapeze(int x, int y, int x1, int y1, int x2, int y2) {
        float A = x - x1;
        float B = y - y1;
        float C = x2 - x1;
        float D = y2 - y1;
        float E = -D;
        float F = C;
        float dot = A * E + B * F;
        float len_sq = E * E + F * F;

        return (float) ((float) Math.abs(dot) / Math.sqrt(len_sq));
    }

}
