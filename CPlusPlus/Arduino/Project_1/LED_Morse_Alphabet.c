const int pin = 13;
const int d_break = 1000; //digit break
const int l_break = 3000; //letter break
const int w_break = 5000; //word break
const int dot_l = 1000; //lenght of dot
const int dash_l = 3000; //lenght of dot

void setup()
{
  pinMode(pin, OUTPUT);
}

void digit_break()
{
  delay(d_break);
}

void letter_break()
{
  delay(l_break);
}

void word_break()
{
  delay(w_break);
}

void led_off()
{
  digitalWrite(pin, LOW);
}

void dot()
{
  digitalWrite(pin, HIGH);
  delay(dot_l);
  led_off();
}

void dash()
{
  digitalWrite(pin, HIGH);
  delay(dash_l);
  led_off();
}

void which_break(int wordend)
{
  if (wordend == 1) {word_break();};
  if (wordend == 0) {letter_break();};
}

void letter_t(int wordend)
{
  dash();
  which_break(wordend);
}

void letter_o(int wordend)
{
  dash();
  digit_break();
  dash();
  digit_break();
  dash();
  which_break(wordend);
}

void letter_m(int wordend)
{
  dash();
  digit_break();
  dash();
  which_break(wordend);
}

void letter_a(int wordend)
{
  dot();
  digit_break();
  dash();
  which_break(wordend);
}

void letter_s(int wordend)
{
  dot();
  digit_break();
  dot();
  digit_break();
  dot();
  which_break(wordend);
}

void letter_z(int wordend)
{
  dash();
  digit_break();
  dash();
  digit_break();
  dot();
  digit_break();
  dot();
  which_break(wordend);
}

void letter_j(int wordend)
{
  dot();
  digit_break();
  dash();
  digit_break();
  dash();
  digit_break();
  dash();
  which_break(wordend);
}

void letter_n(int wordend)
{
  dash();
  digit_break();
  dot();
  which_break(wordend);
}

void letter_k(int wordend)
{
  dash();
  digit_break();
  dot();
  digit_break();
  dash();
  which_break(wordend);
}

void letter_i(int wordend)
{
  dot();
  digit_break();
  dot();
  which_break(wordend);
}

void letter_e(int wordend)
{
  dot();
  which_break(wordend);
}

void letter_d(int wordend)
{
  dash();
  digit_break();
  dot();
  digit_break();
  dot();
  which_break(wordend);
}


void loop()
{

  //Led will be enabled and disabled in a way that it will show: tomasz jan oksiedzki in morse alphabet
  //-/---/--/.-/.../--..//.---/.-/-.//---/-.-/.../.././-../--../-.-/.//
  word_break();
  letter_t(0);
  letter_o(0);
  letter_m(0);
  letter_a(0);
  letter_s(0);
  letter_z(1);
  letter_j(0);
  letter_a(0);
  letter_n(1);
  letter_o(0);
  letter_k(0);
  letter_s(0);
  letter_i(0);
  letter_e(0);
  letter_d(0);
  letter_z(0);
  letter_k(0);
  letter_i(1);
  word_break();
}