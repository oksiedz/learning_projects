/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package pakiet1.Tklasa1;

/**
 *
 * @author tt
 */
public class THuman {
    
    char sex; //MW //LGBT+

    public THuman(char sex) {
        this.sex = sex;
    }

    public THuman() {
    }

    public char getSex() {
        return sex;
    }

    public void setSex(char sex) {
        this.sex = sex;
    }

    @Override
    public String toString() {
        return "THuman{" + "sex=" + sex + '}';
    }
    
}
