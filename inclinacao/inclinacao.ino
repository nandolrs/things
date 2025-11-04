#include "CFIotMQTT.h"
#include <Arduino_JSON.h>
#include <Arduino.h>

CFIotMQTT cfIotMQTT; 

char thingName[] = "esp8266-v1r1";
char topicPub[] = "esp33/pub"; 
char topicSub[] = "esp33/sub"; 

// declara variaveis

const int interruptorPino = A0; // apelido da porta
  
int leitura;
int angulo;
const int limiteSuperior = 40;
String anguloLiteral="";
 

String JsonGerar(String mac,float velocidademotor ,float temperatura, int leitura, int angulo, String anguloLiteral)
{
    JSONVar jsonClima;

    jsonClima["mac"] = mac;
    jsonClima["velocidademotor"] = velocidademotor;
    jsonClima["temperatura"] = temperatura;
    jsonClima["thingname"] = String(thingName);

    jsonClima["leitura"] = leitura;
    jsonClima["angulo"] = angulo;
    jsonClima["anguloLiteral"] = anguloLiteral;



    String jsonString = JSON.stringify(jsonClima);

    Serial.print("json = ");
    Serial.println(jsonString);

    return jsonString;
}

String DadosObterMQTT(String macID)
{  
  float velocidademotor = 12.34;
  float temperatura =  56.78;


  String msg  = JsonGerar(macID ,velocidademotor ,temperatura, leitura, angulo, anguloLiteral);

  return msg;
}

void setup() {

    // configura  CFIOTMQ

    MQSetup();

    // configura pinos

    pinMode(interruptorPino, INPUT);     // configura pino como SAIDA
}

void loop() {

    // realiza tarefa de leitura

    // leitura = digitalRead(interruptorPino); 
    leitura = analogRead(interruptorPino); 

    // mostra a leitura

    Serial.print("leitura (ms): ");
    Serial.println(leitura);

    // adotamos que está de pé 90 graus

    angulo = 90;
    anguloLiteral = "de pe";

    // mas se não estiver de pé, corrigimos informando que está a 180 graus

    if (leitura < limiteSuperior)
    {
        angulo = 180;
        anguloLiteral = "capotado";

    }
    
    // envia por CFIOTMQ
    
    MQLoop();
}

void MQSetup()
{
    cfIotMQTT.SetarThingName(thingName);
    cfIotMQTT.SetarTopicPub(topicPub);
    cfIotMQTT.SetarTopicSub(topicSub);

    cfIotMQTT.AcaoSetarObterDados(DadosObterMQTT);
    cfIotMQTT.setup();
}

void MQLoop()
{
    cfIotMQTT.loop();
}








