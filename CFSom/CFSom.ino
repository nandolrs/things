
/**************************
    www.usinainfo.com.br 
 **************************/
//Nodemcu ES8266 ESP32 = D2/GPIO16


const int campainhaPin = D2 ; 

#define DO_C  132 
#define RE_D  148 
#define MI_E  165 
#define FA_F  175 
#define SOL_G 198 
#define LA_A  220
#define SI_B  247

int melodia[] = 
{
  DO_C, RE_D, MI_E, FA_F, SOL_G, LA_A, SI_B
};

int duracao[] = 
{
  4, 4, 4, 4, 4, 4, 4
};


  
void setup() 
{
  Serial.begin(9600); 
  Serial.println("--- Iniciou a tocar ---");
  
  Serial.print("sizeof(melodia) = ");
  Serial.println(sizeof(melodia));

  pinMode(campainhaPin, OUTPUT); 


}
 
void loop() 
{
  for (int nota = 0; nota < 7; nota++) 
  {
        int duracaoNota = 1000 / duracao[nota];
        tone(campainhaPin, melodia[nota], duracaoNota);

        // pausa entre notas

        int pausa = duracaoNota * 1.30;
        delay(pausa);     

        // para a nota

        noTone(campainhaPin);
  }

    Serial.println("--- Parou de tocar ---");  

    delay(15000);     

}