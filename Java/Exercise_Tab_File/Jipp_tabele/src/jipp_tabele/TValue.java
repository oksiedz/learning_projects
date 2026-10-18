/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package jipp_tabele;

import java.io.Serializable;

/**
 *
 * @author tt
 */
abstract class TValue implements Serializable {
    String ValueName;
    int count;
    
   abstract public String getDescription();
    
}
