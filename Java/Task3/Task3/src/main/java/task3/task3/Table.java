/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package task3.task3;

import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

/**
 *
 * @author tt
 */
public class Table extends AbstractTableModel {

    private static ArrayList<Point> tab;

    public static ArrayList<Point> getTab() {
        return tab;
    }

    public static void setTab(ArrayList<Point> aTab) {
        tab = aTab;
    }

    public Table() {
        tab = new ArrayList<Point>();
    }

    @Override
    public int getRowCount() {
        return tab.size();
    }

    @Override
    public int getColumnCount() {
        return 2;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {

        Point p = (Point) tab.get(rowIndex);
        return switch (columnIndex) {
            case 0 ->
                p.getX();
            case 1 ->
                p.getY();
            default ->
                "";
        };

    }

    @Override
    public String getColumnName(int column) {
        return switch (column) {
            case 0 ->
                "X";
            case 1 ->
                "Y";
            default ->
                "";
        };
    }
}
