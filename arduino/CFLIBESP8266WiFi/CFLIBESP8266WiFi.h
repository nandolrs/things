/*
  - Language: English
  
    CFLIBWiFi.h - Library for ESP8266WiFi library 
    Created for Fernando Rodrigues (nandolrs.iot@gmail.com)), April 12, 2018.
    Release into the public domain.
  
  - Idioma: Português (Brasil)
  
    CFLIBWiFi.h - Bilbioteca para a biblioteca ESP8266WiFi
    Criado por Fernando Rodrigues (nandolrs.iot@hotmail.com), Abril 12, 2018.
    Liberação em domínio público.
*/

#ifndef CFLIBESP8266WiFi_h
  
  #define CFLIBESP8266WiFi_h
  
  #include "Arduino.h"
  #include <SoftwareSerial.h>
  
  class CFLIBESP8266WiFi
  {
    public:
      CFLIBESP8266WiFi();
      bool    Conectar(int tempo);
      bool    Enviar(char servidor[], int porta, String pagina, String mensagem);
      String  Receber();   
      bool    ServidorIniciar();       
      String  ServidorReceber();
      bool    MensagemEnviar(String mensagem);
      String  ipServidor;       
  private:
  
      char        _redeNome[];
      char        _redeSenha[];
      
      bool        _wifiConectado;
      bool        _wifiEnviado;
      String      _mensagemRecebida;
      
      //WiFiClient  _cliente;    
  };

#endif
