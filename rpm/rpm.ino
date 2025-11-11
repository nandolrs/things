#include "CFIotRPM.h"

CFIotRPM iotRPM = CFIotRPM();

void setup() {
  Serial.begin(9600); 
  iotRPM.setup();

 iotRPM.AcaoSetarDadosReceber(DadosReceber);
}
 
void loop() {
  iotRPM.loop();
}

void DadosReceber(long tempoDecorrido)
{
  Serial.print("tempo1=");
  Serial.println(tempoDecorrido);    
}