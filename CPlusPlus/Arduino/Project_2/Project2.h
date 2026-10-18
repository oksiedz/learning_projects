
//biblioteka do urzadzen i2c
#include <Wire.h>

#include <SPI.h>

//biblioteki do czujnika temperatury, wilgotnosci i cisnienia
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
//biblioteki do oled
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//inicjalizacja biblioteki OLED
Adafruit_SSD1306 display(4); // unused pin

//definicja adresu czujnika temperatury, wilgotnosci i cisnienia
#define BME280_I2C_ADDRESS  0x76

//inicjalizacja biblioteki czujnika temperatury, wilgotnosci, cisnienia
Adafruit_BME280 bme; // hardware SPI


//definicja zmiennych
const int LEDpin = 13;
const int delayTime = 1000;
const float kryt_dyst = 10;
//definiowanie pinow pod czujnik dystansu
const int trigPin = 12;
const int echoPin = 11;


void setup() {

 //wlaczenie pinow
 pinMode (trigPin, OUTPUT);
 pinMode (echoPin, INPUT);
 pinMode (LEDpin, OUTPUT);

 //debug w serial i sprawdzenie statusow czujnika
 Serial.begin(9600);
 while (!Serial);
 Serial.println(" ");
 if (bme.begin(BME280_I2C_ADDRESS) == 0) {
 Serial.println("CNo valid BME280 sensor, check wiring, address, sensor ID!");
 while (1) delay(10);
 }
 display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
 display.clearDisplay();
 display.display();
}

void loop() {
 //odczytanie wskazan i zapisanie do zmiennych
 float temp = bme.readTemperature();
 float wilg = bme.readHumidity();
 float dyst = dystans_cm(temp, wilg);
 //zrzucenie wartosci do debuga
 debug(temp, wilg, dyst);
 //zrzucenie wynikow na ekran
 wyswietl(temp, wilg, dyst);
 //wlaczenie diody gdy obiekt zblizy sie za mocno
 if (dyst<kryt_dyst)
     {
       for(int i = 0; i < 10; i++)
       {
        digitalWrite(LEDpin, HIGH);
        delay(100);
        digitalWrite(LEDpin, LOW);
        delay(100);
       };
     }
 
 delay(delayTime);
}
void debug(float temp, float wilg, float dyst) {
 Serial.print("Temperatura = ");
 Serial.print(temp);
 Serial.println(" *C");
 Serial.print("Wilgotnosc = ");
 Serial.print(wilg);
 Serial.println(" %");
 Serial.print("Dystans = ");
 Serial.print(dyst);
 Serial.println(" cm");
 Serial.println ( );
}
void wyswietl (float temp, float wilg, float dyst) {
 display.clearDisplay();
 display.setTextSize(1);
 display.setTextColor(WHITE);
 display.setCursor(0, 0);
 display.print("Temperatura ");
 display.print(temp);
 display.print(" C");
 display.setCursor(0, 12);
 display.print("Wilgotnosc ");
 display.print(wilg);
 display.print(" %");
 display.setCursor(0, 25);
 display.print("Dystans ");
 display.print(dyst);
 display.print(" cm");
 display.display();
}
float dystans_cm (float temp, float wilg) {
 digitalWrite (trigPin, LOW);
 delayMicroseconds (2);
 digitalWrite (trigPin, HIGH);
 delayMicroseconds (10);
 digitalWrite (trigPin, LOW);
 delayMicroseconds (2);
 int czasPulsu_us = pulseIn (echoPin, HIGH);
 float dzwiek_m_sec = 331.4 + (.606 * temp) + (.0124 * wilg);
 float dzwiek_cm_us = dzwiek_m_sec / 10000.0;
 float dystans_cm = (dzwiek_cm_us * czasPulsu_us) / 2;
 return dystans_cm;
}