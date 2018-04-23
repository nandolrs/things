#include <CFLIBESP8266WiFi.h>

CFLIBESP8266WiFi cflib;

bool wifiConectado;

bool wifiEnviado;

String mensagemRecebida="";

String mensagemRecebidaServidor="";

const int tempo=15*1000;

const bool MODO_SERVIDOR=true; // 0=não; 1=sim

void setup() 
{
  // configura a porta de saída
  
  Serial.begin(9600);

  // verifica a conexão, conecta se não conectado

  if(MODO_SERVIDOR)
  {
    // conecta
    
    wifiConectado = cflib.Conectar(tempo);
    while(!wifiConectado)
    {
      Serial.println(".");
      wifiConectado = cflib.Conectar(tempo);
  
    }

    // inicia servidor

    cflib.ServidorIniciar();
  }

}

void loop() 
{
  delay(5 * 1000);
  Serial.println("Hellow! Word");

  if(wifiConectado)
  {
    Serial.println("wifi conectado.");
  }

  if(cflib.ipServidor != "")
  {
    Serial.println("IP SERVIDOR ->" + cflib.ipServidor);
  }  

  if(mensagemRecebidaServidor != "")
  {
    Serial.println("MENSAGEM RECEBIDA SERVIDOR ->" + mensagemRecebidaServidor);

    if(mensagemRecebidaServidor.indexOf("/IR") >= 0)
    {
      //DirecaoIr();
      Serial.println("DirecaoIr");
    }
    else if (mensagemRecebidaServidor.indexOf("/VOLTAR") >= 0)
    {
      //DirecaoVoltar();
      Serial.println("DirecaoVoltar");
    }
    else if (mensagemRecebidaServidor.indexOf("/ESQUERDA") >= 0)
    {
      //DirecaoEsquerda();
      Serial.println("DirecaoEsquerda");
    }
    else if (mensagemRecebidaServidor.indexOf("/DIREITA") >= 0)
    {
      //DirecaoDireita();
      Serial.println("DirecaoDireita");
    }    
    else if (mensagemRecebidaServidor.indexOf("LIGAR_DESLIGAR") >= 0)
    {
      //DirecaoLigarDesligar();
      Serial.println("DirecaoLigarDesligar");
    }       
  }  
  

  if(!MODO_SERVIDOR)
  {
    if(wifiEnviado)
    {
      Serial.println("mensagem enviada.");
    }   
     
    if(mensagemRecebida != "")
    {
      Serial.println("MENSAGEM ->" + mensagemRecebida);
    }    



    // ...
      
    String inputSerial = Serial.readString();
    if(inputSerial == "conectar" && !wifiConectado)
    {
      
      Serial.println("tentando conectar.");
  
      wifiConectado = cflib.Conectar(tempo);
  
      if(!wifiConectado)
      {
        Serial.println("falha ao tentar conectar.");
      }
      else
      {
        cflib.ServidorIniciar();
        Serial.println("servidor iniciado.");
      }
  
    }else if(inputSerial == "enviar" && wifiConectado)
    {
      
      Serial.println("tentando enviar.");
  
      wifiEnviado = cflib.Enviar("192.168.0.7", 80,"cfwebinterface/iot/ws", "?inbound=012345678&msg=HellowWord"); // .aspx
  
      if(!wifiEnviado)
      {
        Serial.println("falha ao enviar.");
      }
  
    }else if(inputSerial == "receber" && wifiEnviado)
    {
      Serial.println("tentando receber.");
  
      mensagemRecebida = cflib.Receber();

      
    }
  }
  else // (!MODO_SERVIDOR)
  {
    mensagemRecebidaServidor = cflib.ServidorReceber(); 
  }
}
