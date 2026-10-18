/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package pakiet1.Tklasa1;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

/**
 *
 * @author tt
 */
public class Tklasa extends JFrame implements ActionListener{ //klasą nadrzeędną jest JFrame - trzeba dodać import JFrame (extends). implements wskazuje, że dziedziczymy po interfejsie
    
    JButton jb1;//cena klasy to przycisk
    
    Tklasa() //konstruktor tworzy formularz
    {
        setSize(800,600);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);//linijka, która po zamknięciu formularza ma zamknąć działanie programu
        
        
        //chcielibyśmy w oknie zobaczyć jakąś kontrolkę - np. JButton
        JButton jb1 = new JButton("Press me1");
        JButton jb2 = new JButton("Press me2");
        JTextField jb3 = new JTextField("Field");
        
        //istnieją zarządcy ustawienia komponentów - layout manager
        //setLayout(new BorderLayout()); //Pozwala ustawiać północ, południe, wschód, zachód, centrum
        //setLayout(new FlowLayout());//resposnywny interfejs
        setLayout(null);
        jb1.setBounds(10, 10, 100, 20);
        jb2.setBounds(10, 40, 200, 30);
        jb3.setBounds(10, 80, 200, 30);
        jb1.addActionListener(this);
        getContentPane().add(jb1,"Center"); //prawidłowe dodanie buttona do ekranu
        getContentPane().add(jb2, "North");
        getContentPane().add(jb3, "North");
        setVisible(true);
    }
    
    
    
    static int StrToInt (String abc)
    {
        return Integer.parseInt(abc);
    }
    
    int StrToInt2 (String abc)
    {
        return Integer.parseInt(abc);
    }
    
    public static void main (String[] args){
        
        System.out.println("hello");
        System.out.println("hello2");
        System.out.println("Empty line");
        
        //zadanie: zliczyć dane, które podane są jako argumenty - w Run/Set Porject configuration/Customise/run
        String a = "123";
        int b = Integer.parseInt(a); //tak się parsuje pojedyncze wartości
        System.out.println(""+b);
        
        //przykład wykorzystania niestatycznej metody
        Tklasa k1 = new Tklasa();
        
        int sum = 0; //zmienna do wyliczania sumy argumentów
        int sum2 = 0;
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            System.out.println(""+args[i]);
            
            sum = sum + StrToInt(arg);
            sum2 += k1.StrToInt2(arg);
            
            if (i + 1 == args.length)
            {
                System.out.println("Suma argumentów wynosi: " + sum);
                System.out.println("Suma argumentów policzona z wykorzystaniem metody niestatycznej wynosi: " + sum2);
            }
            
        }
        
            //powołanie obiektu z klasy2
    TPerson p1 = new TPerson("123","12.5","Alicja","W");
    TPerson p2 = new TPerson("123","12.5","Arek","M");
        
    //p1.age = 12; - niedostępne, gdy age stał się prywatny - trzeba ustawiać za pomocą setAge.
    //p2.age = 13;
    p1.setAge(12, 1);
    p2.setAge(131, 2);
    
    System.out.println("info o obiekcie: "+p1.getAge() + ", " + p1.getHeight());
    System.out.println(""+p1); //to wywołuje metodę to_string - który to przeciążą bo w TPERson zrobiliśmy To string
    System.out.println(""+p2.toString());
    }

    @Override //przeciążona metoda z interfejsu actionPerformed
    public void actionPerformed(ActionEvent e) {
        System.out.append("Pressed - thanks.");
    }
}

