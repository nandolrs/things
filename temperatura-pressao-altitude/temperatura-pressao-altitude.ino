#include <Adafruit_BMP085.h>
#include <Arduino_JSON.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFiMulti.h>
#include <WiFiClientSecureBearSSL.h>

#include "certs.h"

#ifndef STASSID
#define STASSID "nandonet"
#define STAPSK "08111969"
#endif

ESP8266WiFiMulti WiFiMulti;

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

//char ssid[] = "Silva_2G";          //  your network SSID (name)
//char pass[] = "16011999";   // your network password

char ssid[] = "nandonet";          //  your network SSID (name)
char pass[] = "08111969";   // your network password

int status = WL_IDLE_STATUS;

WiFiServer server(80);

String msg = "";

int protocoloPost=0; // 0=get, 1=post
int protocoloSSL=1; // 0= http, 1=https

int serverPort = 80;

//String serverNamePost = "http://192.168.0.91:8000/api/meteorologia";
//String serverNameGet = "http://192.168.0.91:8000/api";

//String serverNamePost = "http://192.168.0.91:35145/api/meteorologia";
//String serverNameGet = "http://192.168.0.91:35145/api";

//String serverNamePost = "http://192.168.0.81:8000/api/meteorologia";
//String serverNameGet = "http://192.168.0.81:8000/api";

//String serverNamePost = "http://192.168.0.81:35145/api/meteorologia";
//String serverNameGet = "http://192.168.0.81:35145/api";

String serverNamePost = "https://meteorologia.negritando.com/api/meteorologia";
String serverNameGet = "https://meteorologia.negritando.com/api";

//String serverNamePost = "localhost:5094/api/meteorologia";
//String serverNameGet = "localhost:5094/api";

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

    jsonClima["temperatura"] = temperatura;
    jsonClima["pressao"] = pressao;
    jsonClima["altitude"] = altitude;
    jsonClima["dispositivoNome"] = "esp8266";

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
    int httpResponseCode;

    if(protocoloPost==1)
    {
      Serial.print("url = ");
      Serial.println(serverNamePost);

      http.begin(client, serverNamePost, serverPort);
      httpResponseCode = http.POST(msg);
    }
    else
    {
      Serial.print("serverNameGet = ");
      Serial.println(serverNameGet);
      
      Serial.print("serverPort = ");
      Serial.println(serverPort);

      http.begin(client, serverNameGet,serverPort);
      httpResponseCode = http.GET();
    }
    http.addHeader("Content-Type", "text/plain" ); // text/plain; charset=utf-8   "application/json"
    Serial.println(httpResponseCode);

    if(httpResponseCode > 0)
    {
      String payload = http.getString();
      Serial.println(payload);
    }
    else
    {
      Serial.printf("[HTTPS] GET... failed, error: %s\n", http.errorToString(httpResponseCode).c_str());


    }

    http.end();

    delay(3000);
}

void setup_wifi_ssl() {

  Serial.begin(9600); // 115200
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(STASSID, STAPSK);
  Serial.println("setup() done connecting to ssid '" STASSID "'");
}

void loop_wifi_ssl() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    std::unique_ptr<BearSSL::WiFiClientSecure> client(new BearSSL::WiFiClientSecure);

    //client->setFingerprint(fingerprint_negritando_com_certificado); //  fingerprint_sni_cloudflaressl_com
    // Or, if you happy to ignore the SSL certificate, then use the following line instead:
    client->setInsecure();

    HTTPClient https;

    String serverName = "";
    if(protocoloPost==1)
    {
      serverName  = serverNamePost;
    }
    else
    {
      serverName  = serverNameGet;
    }

    Serial.print("[HTTPS] begin...\n");
    if (https.begin(*client, serverName, jigsaw_port)) {  // jigsaw_host ,HTTPS

      Serial.print("url = ");
      Serial.println(serverName);

      Serial.print("porta = ");
      Serial.println(jigsaw_port);

      Serial.print("[HTTPS] GET...\n");
      // start connection and send HTTP header

      int httpCode = -1;
      if(protocoloPost==1)
      {
        httpCode = https.POST(msg);
      }
      else
      {
        httpCode = https.GET();
      }

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = https.getString();
          // String payload = https.getString(1024);  // optionally pre-reserve string to avoid reallocations in chunk mode
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }

      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }
  }

  Serial.println("Wait 10s before next round...");
  delay(10000);
}


void setup()
{
  serverPort = 80;
  if(protocoloSSL==1)
  {
    serverPort = 443;
  }

  if(protocoloSSL==0)
  {
    setup_wifi();
  }
  else
  {
        setup_wifi_ssl();
  }

  setup_clima();
}

void loop()
{
  loop_clima();

  if(protocoloSSL==0)
  {
    loop_wifi();
  }
  else
  {
    loop_wifi_ssl();
  }
}