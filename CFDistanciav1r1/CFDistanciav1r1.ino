/**************************
       Usinainfo
  www.usinainfo.com.br 
 **************************/

const int trigPin = 4;// D2;// 22;
const int echoPin = 5;// D1; //21;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;

void setup() {
  Serial.begin(115200); 
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
}

void loop() {
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  

  duration = pulseIn(echoPin, HIGH);
  
 distanceCm = duration * SOUND_SPEED/2;
  
  Serial.print("Distancia (cm): ");
  Serial.println(distanceCm);
  
  delay(1000);
}
