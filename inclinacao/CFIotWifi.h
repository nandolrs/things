#ifndef CFIotWifi_H
#define CFIotWifi_H

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

class CFIotWifi {
  public:
    CFIotWifi();  //  Constructor 
    String  CFIotWifiConectar();
    void CFIotWifiRelogioAtualizar();
    void CFIotWifiX509Configurar();
    String CFIotWifiRelogioAtualizarMacBuscar();

    WiFiClientSecure _net;    
    ESP8266WiFiClass _wifi; // Store the reference

  private:
    String _macID;
    // ESP8266WiFiClass& _wifi; // Store the reference


};

#endif