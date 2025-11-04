#include "CFIotWifi.h"
#include "secrets-iotwifi.h"

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

// The server which will require a client cert signed by the trusted CA

BearSSL::X509List cert(AWS_CERT_CA);
BearSSL::X509List client_crt(AWS_CERT_CRT);
BearSSL::PrivateKey key(AWS_CERT_PRIVATE);

CFIotWifi::CFIotWifi() // char* publishTopic 
{
  _net = WiFiClientSecure();

}

String CFIotWifi::CFIotWifiConectar()
{
    _wifi.mode(WIFI_STA); /// ??? WiFi
    _wifi.begin(WIFI_SSID, WIFI_PASSWORD);

    String mac = _wifi.macAddress();
    _macID = mac;

    Serial.println("Connecting to Wi-Fi");

    while (_wifi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }

    return mac;
}

void CFIotWifi::CFIotWifiRelogioAtualizar() {
  
  const char* ntpServer1 = "pool.ntp.org";
  const char* ntpServer2 = "time.nist.gov";
  
  // const char* ntpServer1 = "pool.ntp.br";
  // const char* ntpServer2 = "pool.ntp.br";

  // const char* ntpServer1 = "a.st1.ntp.br";
  // const char* ntpServer2 = "b.st1.ntp.br";
  
  const long  gmtOffset_sec = 3600;
  const int   daylightOffset_sec = 3600;  
  // configTime(3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
    configTime(3 * 3600, 0, ntpServer1, ntpServer1);

  // configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    Serial.print("ntpServer1,ntpServer2=");
    Serial.print(ntpServer1);
    Serial.print(",");
    Serial.println(ntpServer2);

    
    now = time(nullptr);
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));
}

void CFIotWifi::CFIotWifiX509Configurar()
{
    _net.setTrustAnchors(&cert);
    _net.setClientRSACert(&client_crt, &key);
}

String CFIotWifi::CFIotWifiRelogioAtualizarMacBuscar()
{
  return _macID;
}    


