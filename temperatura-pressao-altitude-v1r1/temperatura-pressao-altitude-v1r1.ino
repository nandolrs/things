#include "secrets.h"
#include <WiFiClientSecure.h>
//#include <WiFiClientSecureBearSSL.h>

#include <MQTTClient.h>
#include <ArduinoJson.h>
//#include <Arduino_JSON.h>
//#include "WiFi.h"
#include <ESP8266WiFi.h>


// The MQTT topics that this device should publish/subscribe
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"

// The server which will require a client cert signed by the trusted CA
BearSSL::WiFiServerSecure server(443);


WiFiClientSecure net = WiFiClientSecure();
MQTTClient client = MQTTClient(256);

void ServerSetup()
{
  // Attach the server private cert/key combo
  BearSSL::X509List *serverCertList = new BearSSL::X509List(AWS_CERT_CRT ); // server_cert
  BearSSL::PrivateKey *serverPrivKey = new BearSSL::PrivateKey( AWS_CERT_PRIVATE ); // server_private_key

  // Require a certificate validated by the trusted CA
  BearSSL::X509List *serverTrustedCA = new BearSSL::X509List(AWS_CERT_CA); //  ca_cert
  server.setClientTrustAnchor(serverTrustedCA);

  // Actually start accepting connections
  server.begin();

 net = server.accept();
}

void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  // Configure WiFiClientSecure to use the AWS IoT device credentials
  //net.setCACert(AWS_CERT_CA);
  //net.setCertificate(AWS_CERT_CRT);
  //net.setPrivateKey(AWS_CERT_PRIVATE);

  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.begin(AWS_IOT_ENDPOINT, 8883, net);

  // Create a message handler
  client.onMessage(messageHandler);

  Serial.print("Connecting to AWS IOT");

  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }

  if(!client.connected()){
    Serial.println("AWS IoT Timeout!");
    return;
  }

  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

  Serial.println("AWS IoT Connected!");
}

void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["time"] = millis();
  doc["sensor_a0"] = analogRead(0);
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client

  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}

void messageHandler(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);

//  StaticJsonDocument<200> doc;
//  deserializeJson(doc, payload);
//  const char* message = doc["message"];
}

void setup() {
  Serial.begin(9600);
  connectAWS();
}

void loop() {
  publishMessage();
  client.loop();
  delay(1000);
}
