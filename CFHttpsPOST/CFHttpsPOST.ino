/*
    HTTP over TLS (HTTPS) example sketch

    This example demonstrates how to use
    WiFiClientSecure class to access HTTPS API.
    We fetch and display the status of
    esp8266/Arduino project continuous integration
    build.

    Created by Ivan Grokhotkov, 2015.
    This example is in public domain.

    -- Arduino :: menu :: file :: preferences :: adicional boards manager url

      http://arduino.esp8266.com/stable/package_esp8266com_index.json
      https://dl.espressif.com/dl/package_esp32_index.json

    -- Arduino :: menu :: sketch :: include library :: manage libraries :: 

      https://arduinojson.org/?utm_source=meta&utm_medium=library.properties

      https://github.com/256dpi/arduino-mqtt
*/

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>



// https://www.negritando.com
// CN: Amazon Root CA 1
// not valid before: 25/05/2015, 21:00:00 GMT-30
// not valid after:  16/01/2038, 21:00:00 GMT-3
const char cert_DigiCert_Global_Root_CA [] PROGMEM = R"CERT(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)CERT";

const char* github_host = "meteorologia.negritando.com";
                           
const uint16_t github_port = 443;

const char* ssid = "Silva_2G";
const char* password = "16011999";

X509List cert(cert_DigiCert_Global_Root_CA);

void setup() {
  Serial.begin(9600);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Set time via NTP, as required for x.509 validation
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

  // Use WiFiClientSecure class to create TLS connection
  WiFiClientSecure client;
  Serial.print("Connecting to ");
  Serial.println(github_host);

  Serial.printf("Using certificate: %s\n", cert_DigiCert_Global_Root_CA);
  client.setTrustAnchors(&cert);

  if (!client.connect(github_host, github_port)) {
    Serial.println("Connection failed");
    return;
  }

  String url = "/api/clima";
  Serial.print("Requesting URL: ");
  Serial.println(url);

  String output = JsonGerar();

  // client.println(String("POST ") + url +" HTTP/1.1");
  // client.println("Host: " + String(github_host));
  // client.println("Content-Type: application/json" );
  // client.println("Content-Length: " + output.length() );
  // client.println();
  // client.println(output + "\n");

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                 "Host: " + String(github_host) + "\r\n" +
                 //"Connection: close\r\n" +
                 "Content-Type: application/json\r\n" +
                 "Content-Length: " + output.length() + "\r\n" +
                 "\r\n" + // This is the extra CR+LF pair to signify the start of a body
                 output + "\n");  


  Serial.println("----- lendo inicio -------");
  Serial.println(output);
  Serial.println("----- lendo final -------");

  Serial.println("----- lendo inicio -------");
  Serial.println(JsonObter(client));
  Serial.println("----- lendo final -------");

}

String JsonGerar()
{
  // Allocate the JSON document
  JsonDocument doc;

  // Add values in the document
  doc["id"] = 0;
  doc["nome"] = "ESP32";
  doc["pressao"] = 56.78D;
  doc["temperatura"] = 67.89D;
  doc["umidade"] = 78.90D;

  String out;
  serializeJson(doc, out);

  return out;

}

String JsonObter(BearSSL::WiFiClientSecure cliente)
{
  String desprezado = cliente.readStringUntil('{'); 
  String json = '{' +  cliente.readString(); 
  return json;
}

void loop() {}
