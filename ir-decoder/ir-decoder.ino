#include <string.h>

// 0x00 Super key
// 0x01 escape
// 0x02 enter
// 0x03 fullscreen
// 0x04 page up
// 0x05 page down
// 0x06 volume+
// 0x07 volume-

const int irPin = 9;

//                Power-  up - left  -right -down- OK - mute   - 1 -    2 -    3 -    4 -     5 -    6 -    7 -    8 -    9 -     0 -  ch+-   ch- - vol+ - vol-
int keymap[21] = {11789, 2034, 18930, 19443, 2545, 3058, 14348, 16907, 17419, 17932, 18443, 18956, 19468, 19981, 20491, 21004, 16394, 12812, 1229, 15373, 15886};

void setup() {
  Serial.begin(115200);
  pinMode(irPin, INPUT);
}

void loop() {
  int key = getIrKey();
  
  if (key != 0) {
    for (int i = 0; i < 21; i++) {
      if (key == keymap[i]) {
        switch (keymap[i]) {
          case 11789:
            exe("shutdown /s /t 0");
            break;
          case 16907:
            exe("chrome");
            ful();
            break;
          case 17419:
            exe("osk");
            break;
          case 3058:
            move(0x12);
            break;
          case 15373:
            vol('+', 5);
            break;
          case 15886:
            vol('-', 5);
            break;
          case 18930:
            move(0x10);
            break;
          case 19443:
            move(0x11);
            break;
          case 2034:
            move(0x08);
            break;
          case 2545:
            move(0x09);
            break;
        }
        break; // Salir del for cuando encuentre la tecla
      }
    }
  }
  
  delay(150); // CAMBIO: era 1000, ahora 150
}

int getIrKey() {
  int len = pulseIn(irPin, LOW);
  int key, temp;
  key = 0;
  
  if (len > 5000) {
    for (int i = 1; i <= 32; i++) {
      temp = pulseIn(irPin, HIGH);
      if (temp > 1000)
        key = key + (1 << (i - 17));
    }
  }
  
  if (key < 0)
    key = -key;
  
  delay(100); // CAMBIO: era 250, ahora 100
  return key;
}

int move(byte i) {
  Serial.write(i);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int sendText(char* tx) {
  Serial.write(tx);
  Serial.write(0x02);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int exe(char* tx) {
  Serial.write(0x00);
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write("r");
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write(tx);
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write(0x02);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int ful() {
  Serial.write(0x03);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int vol(char v, int cant) {
  byte vol;
  if (v == '+') {
    vol = 0x06;
  } else if (v == '-') {
    vol = 0x07;
  }
  
  for (int i = 0; i < cant; i++) { // ARREGLADO: faltaba i=0
    Serial.write(vol);
    delay(150); // CAMBIO: era 300, ahora 150
  }
  return 0;
}