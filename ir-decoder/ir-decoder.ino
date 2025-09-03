#include <string.h>
// 0x00 Super key
// 0x01 escape
// 0x02 enter
// 0x03 fullscreen
// 0x04 page up
// 0x05 page down 
// 0x06 volume+
// 0x07 volume-
//definimo el pin del sensor infrarrojo
const int irPin = 9;
//                Power- up - left-right-down- OK - mute-  1  -  2  -  3  -  4  -  5  -  6  -  7  -  8  -  9  -  0  -ch+- ch- - vol+ - vol- // 
int keymap[21] = {11789,2034,18930,19443,2545,3058,14348,16907,17419,17932,18443,18956,19468,19981,20491,21004,16394,12812,1229,15373,15886};
void setup() 
{  
  Serial.begin(115200);
  //Usamos el pin como input para recibir la información
  pinMode(irPin, INPUT);
}

void loop() 
{
  //guardamos el resultado de la funcion en una variable
  int key = getIrKey();
  //Ninguna señal recibida
  if(key != 0)
  {
    //Serial.println(key);
    for(int i=0; i<21 ; i++)
    {
      if(key==keymap[i])
      {
        switch(keymap[i])
        {
          case 11789:
            exe("shutdown /s /t 0");
            break;
          case 16907:
            exe("chrome");
            ful();
            break;

        }
      }
    }
  }
  
  delay(1000);
}

int getIrKey()
{
  //apagamos el pin y recibimos los datos
  int len = pulseIn(irPin,LOW);
  int key, temp;
  key = 0;
  //---Serial.print("len=");
  //---Serial.println(len);
  //verificamos si la señal entra en el espectro del IR
  if(len > 5000) 
  {
    //ciclo para guardar los bits de la señal
    for(int i=1;i<=32;i++)
    {
      temp = pulseIn(irPin,HIGH);
      if(temp > 1000)
        key = key + (1<<(i-17));
    }
  }
  if(key < 0 )
    //resta los bits negativos
    key = -key;

  delay(250);
  return key;
}

int sendText(char* tx)
{
  Serial.write(tx);
  Serial.write(0x02);
  delay(500);

  return 0;
}
int exe(char* tx)
{
  Serial.write(0x00);
  delay(500);
  Serial.write("r");
  delay(500);
  Serial.write(tx);
  delay(500);
  Serial.write(0x02);
}
int ful()
{
  Serial.write(0x03);
  delay(500);
}