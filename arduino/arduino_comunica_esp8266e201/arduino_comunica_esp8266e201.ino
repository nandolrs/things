#include <SoftwareSerial.h>

const int _PINO_TX = 1; // 7
const int _PINO_RX = 0; // 6
const int _PINO_DIREITA = 9;
const int _PINO_ESQUERDA = 8;
const int _PINO_IR_VOLTAR = 7;//IR=0, VOLTAR=1;

int estadoLigado = false;
int estadoIr = true;

SoftwareSerial portaSerial(_PINO_RX, _PINO_TX);

const int SERIAL_VELOCIDADE=9600;

void setup() 
{
  Serial.begin(SERIAL_VELOCIDADE);
  portaSerial.begin(SERIAL_VELOCIDADE);

  pinMode(_PINO_RX, INPUT);
  pinMode(_PINO_TX, OUTPUT);

  pinMode(_PINO_DIREITA, OUTPUT);
  pinMode(_PINO_ESQUERDA, OUTPUT);
}

void loop() 
{
    
  if(portaSerial.available() > 0) // 
  {
    //Serial.println("lendo ... ");

    String frase = "";
    while(portaSerial.available() > 0) // portaSerial
    {
      frase += portaSerial.readString(); // portaSerial
    }
    Serial.print(frase);

    // decide o comando

    if(frase.indexOf("/IR") >= 0)
    {
      DirecaoIr();
    }
    else if (frase.indexOf("/VOLTAR") >= 0)
    {
      DirecaoVoltar();
    }
    else if (frase.indexOf("/ESQUERDA") >= 0)
    {
      DirecaoEsquerda();
    }
    else if (frase.indexOf("/DIREITA") >= 0)
    {
      DirecaoDireita();
    }    
    else if (frase.indexOf("LIGAR_DESLIGAR") >= 0)
    {
      DirecaoLigarDesligar();    
    }       
  }

}

void DirecaoDireita()
{
  //Serial.println("arduino.DirecaoDireita");
  digitalWrite(_PINO_DIREITA, HIGH);
  digitalWrite(_PINO_ESQUERDA, LOW);  
}

void DirecaoEsquerda()
{
  //Serial.println("arduino.DirecaoEsquerda");
  digitalWrite(_PINO_DIREITA, LOW);
  digitalWrite(_PINO_ESQUERDA, HIGH);  
}

void DirecaoIr()
{
  estadoIr = true;
  //Serial.println("arduino.DirecaoIr");
  digitalWrite(_PINO_IR_VOLTAR, HIGH);

  DirecaoEsquerda();
  DirecaoDireita();

}

void DirecaoVoltar()
{
  estadoIr = false;
  //Serial.println("arduino.DirecaoVoltar");
  digitalWrite(_PINO_IR_VOLTAR, LOW);
}

void DirecaoLigarDesligar()
{
  Serial.println("arduino.DirecaoLigarDesligar");
  if(estadoLigado)
  {
    digitalWrite(_PINO_DIREITA, LOW);
    digitalWrite(_PINO_ESQUERDA, LOW);      
  }
  else
  {
    digitalWrite(_PINO_DIREITA, HIGH);
    digitalWrite(_PINO_ESQUERDA, HIGH);       
  }

  estadoLigado = !estadoLigado;
}
