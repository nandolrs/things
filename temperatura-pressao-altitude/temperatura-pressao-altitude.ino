#include <Adafruit_BMP085.h>
#include <Arduino_JSON.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>




/*************************************************** 
  This is an example for the BMP085 Barometric Pressure & Temp Sensor

  Designed specifically to work with the Adafruit BMP085 Breakout 
  ----> https://www.adafruit.com/products/391

  These pressure and temperature sensors use I2C to communicate, 2 pins
  are required to interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

// Connect VCC of the BMP085 sensor to 3.3V (NOT 5.0V!)
// Connect GND to Ground
// Connect SCL to i2c clock - on '168/'328 Arduino Uno/Duemilanove/etc thats Analog 5
// Connect SDA to i2c data - on '168/'328 Arduino Uno/Duemilanove/etc thats Analog 4
// EOC is not used, it signifies an end of conversion
// XCLR is a reset pin, also not used here

Adafruit_BMP085 bmp;

char ssid[] = "nandonet";          //  your network SSID (name)
char pass[] = "08111969";   // your network password
String serverNamePost = "http://localhost:5041/api/meteorologia/";
//String serverNameGet = "http://localhost:35145/api/meteorologia/<dispositivoNome>";
String serverNameGet = "https://www.negritando.com/temperatura-pressao-altitude/medidor.json";



int status = WL_IDLE_STATUS;

WiFiServer server(80);

String msg = "";




String JsonGerar(float temperatura, float pressao, float altitude)
{

    Serial.println("*********");

    Serial.print("temperatura = " );
    Serial.println(temperatura);

    Serial.print("pressao = " );
    Serial.println(pressao);

    Serial.print("altitude = " );
    Serial.println(altitude);


    JSONVar jsonClima;

    jsonClima["temperatura"] = (float) temperatura;
    jsonClima["pressao"] = pressao;
    jsonClima["altitude"] = altitude;

    String jsonString = JSON.stringify(jsonClima);

    Serial.print("json = ");
    Serial.println(jsonString);


    return jsonString;
}

void setup_clima() {
  Serial.begin(9600);
  if (!bmp.begin()) {
	Serial.println("Could not find a valid BMP085 sensor, check wiring!");
	while (1) {}
  }
}

void loop_clima()
{
  msg = JsonGerar(
    bmp.readTemperature()
    ,bmp.readPressure()
    ,bmp.readAltitude()
  );
}


  
void loop1() {
    Serial.print("Temperature = ");
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");
    
    Serial.print("Pressure = ");
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");
    
    // Calculate altitude assuming 'standard' barometric
    // pressure of 1013.25 millibar = 101325 Pascal
    Serial.print("Altitude = ");
    Serial.print(bmp.readAltitude());
    Serial.println(" meters");

    Serial.print("Pressure at sealevel (calculated) = ");
    Serial.print(bmp.readSealevelPressure());
    Serial.println(" Pa");

  // you can get a more precise measurement of altitude
  // if you know the current sea level pressure which will
  // vary with weather and such. If it is 1015 millibars
  // that is equal to 101500 Pascals.
    Serial.print("Real altitude = ");
    Serial.print(bmp.readAltitude(101500));
    Serial.println(" meters");
    
    Serial.println();
    delay(500);
}




void setup_wifi()
{
  Serial.begin(9600);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());
  server.begin();


}

void loop_wifi()
{
    Serial.println("connected");
    Serial.print("msg = ");
    Serial.println(msg);

    WiFiClient client = server.accept();

    HTTPClient http;
    http.begin(client, serverNameGet);
    //http.begin(client, serverNamePost);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(msg);
    //int httpResponseCode = http.GET();
    Serial.println(httpResponseCode);

    if(httpResponseCode > 0)
    {
      String payload = http.getString();
      Serial.println(payload);
    }




    http.end();

    delay(3000);

}


void setup()
{
  setup_wifi();

  setup_clima();
}

void loop()
{
  loop_clima();

  loop_wifi();

}