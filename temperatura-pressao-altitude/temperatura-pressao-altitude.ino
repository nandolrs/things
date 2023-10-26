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

char ssid[] = "Silva_2G";          //  your network SSID (name)
char pass[] = "16011999";   // your network password

String serverNamePost = "http://192.168.0.91:8000/api/meteorologia";
String serverNameGet = "http://192.168.0.91:8000/api";

//String serverNamePost = "http://192.168.0.91:35145/api/meteorologia";
//String serverNameGet = "http://192.168.0.91:35145/api";



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
    //http.begin(client, serverNameGet);
    http.begin(client, serverNamePost);
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