#ifndef CFIotRPM_H
#define CFIotRPM_H

#include <Arduino.h>

typedef void (*FuncaoGenerica)(long tempoDecorrido);


class CFIotRPM {
  public:
    CFIotRPM(); // Constructor

    void setup();
    void loop();

    void AcaoSetarDadosReceber(FuncaoGenerica acaoDadosEnviar);
    void CalcularRPM(long leitura);


  private:
    const int _interruptorPino = A0; // nodemcu esp32 D1;
      
    long _duracao;

    long _leitura;
    long _leituraAnterior;
    const long _leituraLimite=300;


    unsigned long _tempo;
    unsigned long _tempoAnterior;
    unsigned long _tempoDecorrido;    
    
    FuncaoGenerica _acaoDadosReceber;
};



#endif