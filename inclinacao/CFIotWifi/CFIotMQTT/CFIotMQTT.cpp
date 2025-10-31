#include "CFIotMQTT.h"
#include "CFIotWifi.h"

#include "secrets-iotmqtt.h"

#include <ArduinoJson.h>

#include <MQTTClient.h>
#include <WiFiClientSecure.h>

// The MQTT topics that this device should publish/subscribe

CFIotMQTT::CFIotMQTT() // constructor
{
  _cfIotWifi = CFIotWifi(); // publishTopic
  mqttClient = MQTTClient(256);
}

void CFIotMQTT::MQTTConectar(char topic[])
{
    // Connect to the MQTT broker on the AWS endpoint we defined earlier
    mqttClient.begin(AWS_IOT_ENDPOINT, 8883, _cfIotWifi._net); // ??? _wifi _net

    // Create a message handler
    // mqttClient.onMessage(MqttMessageHandler); // <?>

    Serial.print("Connecting to AWS IOT");
    Serial.print("AWS_IOT_ENDPOINT=");
    Serial.println(AWS_IOT_ENDPOINT);

    while (!mqttClient.connect(_thingName))  // THINGNAME
    {
      Serial.print(".");
      delay(100);
    }

    if(!mqttClient.connected()){
      Serial.println("AWS IoT Timeout!");
    }

    // Subscribe to a topic
    mqttClient.subscribe(topic); // topic

    Serial.println("AWS IoT Connected!");  
}

void CFIotMQTT::MQTTLoop()
{
    mqttClient.loop();
}

void CFIotMQTT::MQTTPublicar(char topic[], char jsonBuffer[])
{
  bool retorno = mqttClient.publish(topic,jsonBuffer);
}


void CFIotMQTT::publishMessage(String msgJson)
{
  int i =  msgJson.length()+1;

  char msgJson_[i];
  msgJson.toCharArray(msgJson_, i);  

  MQTTPublicar(_topicPub, msgJson_); // publishTopic jsonBuffer
}

void CFIotMQTT::MQTTMessageHandler(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);

//  StaticJsonDocument<200> doc;
//  deserializeJson(doc, payload);
//  const char* message = doc["message"];
}

void CFIotMQTT::SetarThingName(char* thingName)
{
  _thingName = thingName;
}

void CFIotMQTT::SetarTopicPub(char* topicPub)
{
  _topicPub = topicPub;
}


void CFIotMQTT::SetarTopicSub(char* topicSub)
{
  _topicSub = topicSub;
}

void CFIotMQTT::setup() {
    Serial.begin(9600);

    _macID = _cfIotWifi.CFIotWifiConectar();

    _cfIotWifi.CFIotWifiRelogioAtualizar(); // Required for X.509 validation

    _cfIotWifi.CFIotWifiX509Configurar();

    MQTTConectar(_topicSub); 
}

void CFIotMQTT::loop() {

  String dadosJson = _acaoObterDados(_macID);

  publishMessage(dadosJson);
  MQTTLoop();
  
  delay(1000);
}


void CFIotMQTT::AcaoSetarObterDados(FuncaoGenerica acaoObterDados)
{
  _acaoObterDados = acaoObterDados;
}







