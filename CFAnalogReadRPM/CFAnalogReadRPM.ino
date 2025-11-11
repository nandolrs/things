const int interruptorPino = A0; // nodemcu esp32 D1;
  
long duracao;

long leitura;
long leituraAnterior;
const long leituraLimite=300;


unsigned long tempo;
unsigned long tempoAnterior;
unsigned long tempoDecorrido;


 
void setup() {
  Serial.begin(9600); 
  pinMode(interruptorPino, INPUT); 

  tempoAnterior = millis();

}
 

void loop() {
  leitura = analogRead(interruptorPino); 
  CalcularRPM(leitura);
}

void CalcularRPM(long leitura)
{

  if (leitura < leituraLimite and leituraAnterior > leituraLimite) 
  {
    tempo = millis();
    tempoDecorrido = tempo - tempoAnterior;
    Serial.print("tempo=");
    Serial.println(tempoDecorrido);    
    tempoAnterior = tempo;
  }

  leituraAnterior = leitura;

}





