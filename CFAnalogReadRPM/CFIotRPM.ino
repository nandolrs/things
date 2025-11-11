#include "CFIotRPM.h"

#include <ArduinoJson.h>

// The MQTT topics that this device should publish/subscribe

CFIotRPM::CFIotRPM() // constructor
{
  _cfIotWifi = CFIotWifi(); // publishTopic
  mqttClient = MQTTClient(256);
}


void CFIotRPM::setup() {
    Serial.begin(9600);

    _macID = _cfIotWifi.CFIotWifiConectar();

    _cfIotWifi.CFIotWifiRelogioAtualizar(); // Required for X.509 validation

    _cfIotWifi.CFIotWifiX509Configurar();

    MQTTConectar(_topicSub); 
}

void CFIotRPM::loop() {

  String dadosJson = _acaoDadosEnviar(_macID);

  if (dadosJson.length() > 0)
  {
    publishMessage(dadosJson);
  }

  MQTTLoop();
  
  delay(1000);
}


void CFIotRPM::AcaoSetarDadosEnviar(FuncaoGenerica acaoDadosEnviar)
{
  _acaoDadosEnviar = acaoDadosEnviar;
}








