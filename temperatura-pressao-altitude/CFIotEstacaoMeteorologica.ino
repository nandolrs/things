#include <Adafruit_BMP085.h>
//#include <ArduinoJson.h>
#include <Arduino_JSON.h>

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

void CFIotEstacaoMeteorologicaConectar() {
  Serial.begin(9600);
  if (!bmp.begin()) {
	Serial.println("Could not find a valid BMP085 sensor, check wiring!");
	while (1) {}
  }
}

String CFIotEstacaoMeteorologicaDadosObter()
{  
  String msg  = JsonGerar(
     bmp.readTemperature()
    ,bmp.readPressure()
    ,bmp.readAltitude()
  );

  return msg;
}
