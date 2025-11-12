#include "CFIotRPM.h"

#include <ArduinoJson.h>

CFIotRPM::CFIotRPM() // constructor
{

}


void CFIotRPM::setup() {
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

    _tempoAnterior = _tempo;

    _acaoDadosReceber(_tempoDecorrido);
  }

  _leituraAnterior = _leitura;

}

void CFIotRPM::AcaoSetarDadosReceber(FuncaoGenerica acaoDadosReceber)
{
  _acaoDadosReceber = acaoDadosReceber;
}








