#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <MQTTClient.h>

// The server which will require a client cert signed by the trusted CA

WiFiClientSecure net = WiFiClientSecure();

BearSSL::X509List cert(AWS_CERT_CA);
BearSSL::X509List client_crt(AWS_CERT_CRT);
BearSSL::PrivateKey key(AWS_CERT_PRIVATE);

// MQTT client

MQTTClient mqttClient = MQTTClient(256);

void CFIotWifiConectar()
{
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    Serial.println("Connecting to Wi-Fi");

    while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }
}

void CFIotWifiRelogioAtualizar() {
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

void CFIotWifiX509Configurar()
{
    net.setTrustAnchors(&cert);
    net.setClientRSACert(&client_crt, &key);
}

void CFIotWifiMQTTConectar()
{
    // Connect to the MQTT broker on the AWS endpoint we defined earlier
    mqttClient.begin(AWS_IOT_ENDPOINT, 8883, net);

    // Create a message handler
    mqttClient.onMessage(MqttMessageHandler);

    Serial.print("Connecting to AWS IOT");

    while (!mqttClient.connect(THINGNAME)) {
      Serial.print(".");
      delay(100);
    }

    if(!mqttClient.connected()){
      Serial.println("AWS IoT Timeout!");
    }

    // Subscribe to a topic
    mqttClient.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

    Serial.println("AWS IoT Connected!");  
}

void CFIotWifiMQTTLoop()
{
    mqttClient.loop();
}

void CFIotWifiMQTTPublicar(char topic[], char jsonBuffer[])
{
  mqttClient.publish(topic,jsonBuffer);
}

