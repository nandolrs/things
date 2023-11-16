#include "secrets.h"
#include <ArduinoJson.h>

// The MQTT topics that this device should publish/subscribe

char publishTopic[] = "esp32/pub";
char subscribeTopic[] = "esp32/sub";

void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["time"] = millis();
  doc["sensor_a0"] = analogRead(0);
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client

  CFIotWifiMQTTPublicar(publishTopic, jsonBuffer);

}

void MqttMessageHandler(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);

//  StaticJsonDocument<200> doc;
//  deserializeJson(doc, payload);
//  const char* message = doc["message"];
}

void setup() {
    Serial.begin(9600);

    CFIotWifiConectar();

    CFIotWifiRelogioAtualizar(); // Required for X.509 validation

    CFIotWifiX509Configurar();

    CFIotWifiMQTTConectar();
}

void loop() {
  publishMessage();
  CFIotWifiMQTTLoop();
  delay(1000);
}
