#ifndef CFIotRPM_H
#define CFIotRPM_H

#include <Arduino.h>

typedef String (*FuncaoGenerica)(String macID);


class CFIotRPM {
  public:
    CFIotRPM(); // Constructor

    void setup();
    void loop();

    void AcaoSetarDadosEnviar(FuncaoGenerica acaoDadosEnviar);

  private:
    // char* _thingName;
    // char* _topicPub;
    // char* _topicSub;

    // String _macID;
    
    FuncaoGenerica _acaoDadosEnviar;
};



#endif