/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package jipp_tabele;

import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

/**
 *
 * @author tt
 */
public class TMyModel extends AbstractTableModel {

    //TGift [] tab = new TGift[0];
    // ArrayList <TGift> tab = new ArrayList<TGift>();
    private static ArrayList<TValue> tab;

    public static ArrayList<TValue> getTab() {
        return tab;
    }

    public static void setTab(ArrayList<TValue> aTab) {
        tab = aTab;
    }

    public TMyModel() {
        tab = new ArrayList<TValue>();
    }

    @Override
    public int getRowCount() {
        return tab.size();
    }

    @Override
    public int getColumnCount() {
        return 5;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
    
      if(tab.get(rowIndex).getClass() == TGift.class)
      { 
        TGift g = (TGift) tab.get(rowIndex);
        switch (columnIndex) {
            case 0:
                return rowIndex + 1;
            case 1:
                return tab.get(rowIndex).getDescription();
            case 2:
                return g.getPrize();
            case 3:
                return g.getForWho();
            case 4:
                return g.getWeight();
            default: return "";
        }
        //return "";
      }
      else
      {
         TGood g = (TGood) tab.get(rowIndex);
          switch (columnIndex) {
            case 0:
                return rowIndex + 1;
            case 1:
                return tab.get(rowIndex).getDescription();
            case 2:
                return g.getSizeX();
            case 3:
                return g.getSizeY();
            case 4:
                return g.getSizeZ();
            default: return "";
        }
        // return "";
      }
    }

    @Override
    public String getColumnName(int column) {
        switch (column) {
            case 0:
                return "LP";
            case 1:
                return "Nazwa";
            case 2:
                return "Cena";
            case 3:
                return "Dla kogo";
            case 4:
                return "Waga";
            default: return "";
        }
    }

}
