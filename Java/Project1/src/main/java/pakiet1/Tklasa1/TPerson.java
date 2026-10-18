/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package pakiet1.Tklasa1;

/**
 *
 * @author tt
 */
public class TPerson  extends THuman{ //extends Object - dziedziczenie po klasie object.

    //W Java wszystko jest domyślnie publiczne
    private int age; //jest dostęp w ramach klasy, ale przy wykorzystaniu nie można bezpośrednio się dostać
    private String name;
    private boolean isAlive;
    private double height;
    //char sex; //MW //LGBT+

    TPerson(int a, double height) {
        super('W');//konstruktor wywoływany z klasy nadrzędnej
        age = a;
        this.height = height; //zmienne mają te same nazwy jak to co jest w obiekcie - stąd this. wskazuje, że jako atrybut obiektu przypisujemy atrybut height.
    }

    //można kliknąć prawym przyciskiem Insert code i constructor
    public TPerson(int age, String name, boolean isAlive, double height, char sex) {
        this(age, height);//jest to zainicjowanie konstrutkora TPerson (int a, double height). - bo skoro mamy prostszy konsttukror to nie ma sensu przypisywać od siebie.
        this.isAlive = isAlive;
        this.height = height;
        //this.sex = sex;
        
        
    }

    //konstruktor z dowolną liczbą argumentów
    public TPerson(String... args) // przy takiej konstrukcji możemy stworzyć konstruktor z liczbą argumentów args, które są stringami
    {
        if (args.length > 0) {
            age = Integer.parseInt(args[0]); // pierwszy argument na wiek
        }
        if (args.length > 1) {
            height = Double.parseDouble(args[1]);
        }
        if (args.length > 2) {
            name = args[2];
        }
        /*if (args.length > 3) {
            sex = args[3].charAt(0);
        }*/
    }

    //wprowadzamy metodę  ustawiająca wiek
    void setAge(int a, int r) //r - rodzaj danych
    {
        if (r == 1) // wiek podany w latach
        {
            age = a;
        }
        if (r == 2) {
            age = a / 12;
        }
    }
    
    int getAge ()
    {
        return age;
    }
    //metody dostępowe można wygenerować za pomocą PPM >> getter, setter i wybrać odpowiednie zmienne
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isIsAlive() {
        return isAlive;
    }

    public void setIsAlive(boolean isAlive) {
        this.isAlive = isAlive;
    }

    public double getHeight() {
        return height;
    }

    public void setHeight(double height) {
        this.height = height;
    }
    
    //PPM - insert code + ToSrtring - i to sprint 
    @Override //slowo kluczowe override oznacza, ze wykorzystujemy nadpisanie metody (przeciążenie) z klasy nadrzędnej, ale wszystkie klasy dziedziczą po klasie Object
    public String toString() {
        return "TPerson{" + "age=" + age + ", name=" + name + ", isAlive=" + isAlive + ", height=" + height + '}';
    }

}
