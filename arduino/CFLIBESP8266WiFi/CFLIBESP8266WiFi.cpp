Receber#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>


/*
  - Language: English
  
    CFLIBESP8266WiFi.h - Library for ESP8266WiFi library 
    Created for Fernando Rodrigues (nandolrs.iot@gmail.com)), April 12, 2018.
    Release into the public domain.
  
  - Idioma: Português (Brasil)
  
    CFLIBESP8266WiFi.h - Bilbioteca para a biblioteca ESP8266WiFi
    Criado por Fernando Rodrigues (nandolrs.iot@hotmail.com), Abril 12, 2018.
    Liberação em domínio público.
*/

#include "Arduino.h"
#include "CFLIBESP8266WiFi.h"
#include "SoftwareSerial.h"

char redeNome[] = "Guilherme";
char redeSenha[] = "16011999";
int  porta = 80;

WiFiClient cliente;    
WiFiServer servidor(porta);

const int _PINO_TX = 4;
const int _PINO_RX = 5;

SoftwareSerial portaSerial(_PINO_RX, _PINO_TX);

CFLIBESP8266WiFi::CFLIBESP8266WiFi()
{
}

bool CFLIBESP8266WiFi::Conectar(int timeOut) // millis:timeOut
{
    int tempo = millis();
    int tempo_final = tempo + timeOut;

    WiFi.mode(WIFI_STA);
    WiFi.begin(redeNome, redeSenha);
    bool _wifiConectado = (WiFi.status() == WL_CONNECTED );
    while(WiFi.status() != WL_CONNECTED && millis() <= tempo_final && !_wifiConectado)
    {
      delay(500);
      Serial.print(".");
    }
 
    _wifiConectado = (WiFi.status() == WL_CONNECTED); 
    return _wifiConectado;  
}

bool CFLIBESP8266WiFi::Enviar(char servidor[], int porta, String pagina, String mensagem)
{
  bool retorno;

  // conectando
  
  bool conectou = cliente.connect(servidor, porta);

  retorno = conectou;
  
  Serial.println("conectou.");

  // enviando
  
//  String _frase = 
//    "GET /" 
//    + pagina 
//    + mensagem*/
//    + "\r\nHTTP/1.0" 
//    + "\r\nHOST: " + servidor
//    + "Connection:close\r\n\r\n)"

  String _frase = 
    "GET /" 
    + pagina 
    + "\r\nHTTP/1.0"; 

  
  Serial.println("enviando -> " + _frase);
  retorno = false;

  cliente.print(_frase);
  
  retorno = true;
  
  return retorno;
}

String CFLIBESP8266WiFi::Receber()
{
  String retorno="";

  while(cliente.connected())
  {
    if(cliente.available())
    {
      // recebe a mensagem
      
      retorno= retorno + cliente.readString();

      // responde a mensagem com eco
      
      cliente.print(retorno);  

      // saida
      
      break;
    }
  }

  // antes de retornar manda para o Atmega o recebido (eco)

  MensagemEnviar(retorno);

  return retorno;
}

bool CFLIBESP8266WiFi::ServidorIniciar()
{
  servidor.begin();
  //Serial.print("Servidor iniciado. IP: ");

  IPAddress ip = WiFi.localIP();
  
  CFLIBESP8266WiFi::ipServidor = "." + String(ip[0])
      + "." + String(ip[1])
      + "." + String(ip[2])
      + "." + String(ip[3]);

  Serial.println("IP SERVIDOR ->" + CFLIBESP8266WiFi::ipServidor);

  // configura a comunicação entre ESP8266 e Atmega

  portaSerial.begin(9600);

  
  return true;
}

String CFLIBESP8266WiFi::ServidorReceber()
{
    // verifica se algum cliente enviou algo
    
    cliente = servidor.available();

    return Receber();
}

bool CFLIBESP8266WiFi::MensagemEnviar(String mensagem)
{
  portaSerial.print(mensagem);

  return true;
}


//String CFLIBESP8266WiFi::ipServidor="";
