#ifndef CFIotMQTT_H
#define CFIotMQTT_H

#include <Arduino.h>
#include <MQTTClient.h>

#include "CFIotWifi.h"

typedef String (*FuncaoGenerica)(String macID);
typedef char* (*FuncaoGenericaSemParametro)();

typedef void (*FuncaoGenericaMQTTMessageHandler)(String topic, String payload);


class CFIotMQTT {
  public:
    CFIotMQTT(); // Constructor

    void MQTTConectar(char topic[]);
    void MQTTLoop();
    void MQTTPublicar(char topic[], char jsonBuffer[]);

    void publishMessage(String msgJson);
    void MQTTMessageHandler(String &topic, String &payload);

    void SetarThingName(char* thingName);
    void SetarTopicPub(char* topicPub);
    void SetarTopicSub(char* topicSub);
    void setup();
    void loop();

    void AcaoSetarDadosEnviar(FuncaoGenerica acaoDadosEnviar);
    void AcaoSetarDadosReceber(FuncaoGenericaMQTTMessageHandler acaoDadosReceber);

  private:
    char* _thingName;
    char* _topicPub;
    char* _topicSub;

    String _macID;
    
    FuncaoGenerica _acaoDadosEnviar;
    FuncaoGenericaMQTTMessageHandler _acaoDadosReceber;


    MQTTClient mqttClient;
    CFIotWifi _cfIotWifi;


};



#endif