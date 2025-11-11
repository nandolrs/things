#include "CFIotRPM.h"

#include <ArduinoJson.h>

// The MQTT topics that this device should publish/subscribe

CFIotRPM::CFIotRPM() // constructor
{

}


void CFIotRPM::setup() {
    // Serial.begin(9600); 
    pinMode(_interruptorPino, INPUT); 

    _tempoAnterior = millis();    
}

void CFIotRPM::loop() {

  _leitura = analogRead(_interruptorPino); 
  CalcularRPM(_leitura);
}

void CFIotRPM::CalcularRPM(long leitura)
{

  if (_leitura < _leituraLimite and _leituraAnterior > _leituraLimite) 
  {
    _tempo = millis();
    _tempoDecorrido = _tempo - _tempoAnterior;
    // Serial.print("tempo=");
    // Serial.println(_tempoDecorrido);    
    _tempoAnterior = _tempo;

    _acaoDadosReceber(_tempoDecorrido);
  }

  _leituraAnterior = _leitura;

}

void CFIotRPM::AcaoSetarDadosReceber(FuncaoGenerica acaoDadosEnviar)
{
  _acaoDadosReceber = acaoDadosEnviar;
}








