//Programa: Sensor de Luminosidade
//Autor: GuiaRobotica

const int LDR = D0 ;            // arduino D4; nodemcu esp32 D0;  A0 Pino analógico que o sensor está conectado
const int luz = D1;             // arduino D6; noedemcu esp32 D1; 13 Pino Referente ao led ou rele
int valorsensor ;               // valor que sera armazenado o valor do LDR
void setup1() {
  Serial.begin(9600); 

  pinMode(luz, OUTPUT);         // Coloca variavel luz é um sinal de saidad
  pinMode(LDR, INPUT);          // Coloca a variavel LDR como entrada
}

void loop1() {
  valorsensor = analogRead(LDR);
  Serial.println(valorsensor);

  if (valorsensor < 500) {      // Se o valor de VALORSENSOR for menos que 500
    digitalWrite(luz, HIGH);  // Ligar rele ou led
  } else {                    // Se não
    digitalWrite(luz, LOW);    // Desligar rele ou led
  }
  delay(1000);                 // Aguarda 100 milisegundos
}

void setup() {
  Serial.begin(9600); 

  pinMode(LDR, INPUT);          // Coloca a variavel LDR como entrada
}

void loop() {
  valorsensor = analogRead(LDR);
  Serial.println(valorsensor);


  delay(1000);                 // Aguarda 100 milisegundos
}