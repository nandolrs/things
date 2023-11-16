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

BearSSL::X509List cert(AWS_CERT_CA);
BearSSL::X509List client_crt(AWS_CERT_CRT);
BearSSL::PrivateKey key(AWS_CERT_PRIVATE);

MQTTClient client = MQTTClient(256);

void setClock() {
  configTime(3 * 3600, 0, "pool.ntp.org", "time.nist.gov");

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));
}

void ServerSetup()
{
    Serial.println("ServerSetup ENTROU");

      setClock();  // Required for X.509 validation


  // Attach the server private cert/key combo
  //BearSSL::X509List *serverCertList = new BearSSL::X509List(AWS_CERT_CRT ); // server_cert
  //BearSSL::PrivateKey *serverPrivKey = new BearSSL::PrivateKey( AWS_CERT_PRIVATE ); // server_private_key
  //server.setRSACert(serverCertList, serverPrivKey);

  // Require a certificate validated by the trusted CA
  //BearSSL::X509List *serverTrustedCA = new BearSSL::X509List(AWS_CERT_CA); //  ca_cert
  //server.setClientTrustAnchor(serverTrustedCA);

  // Actually start accepting connections
  //server.begin();

 //net = server.accept();

 
  net.setTrustAnchors(&cert);
  net.setClientRSACert(&client_crt, &key);

 Serial.println("ServerSetup SAIU");
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

  ServerSetup();  messageHandler

  Serial.print("AWS_IOT_ENDPOINT");
  Serial.println(AWS_IOT_ENDPOINT);

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

  Serial.println("conectou!!!");


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
