/*

1. conectar na mesma rede da COISA
1. abrir o navegador: chrome, mozila, ...
2. para LIGAR deve informar no navegador a url: http://<IP da COISA>/comando=ligar
3. para DESLIGAR deve informar no navegador a url: http://<IP da COISA>/comando=ligar

*/

#include <ESP8266WiFi.h>

const char* ssid = "nandonet"; 
const char* password = "08111969";

const int chaveTactilPin = D0 ; 


WiFiServer server(80);


void setup()
{
  Serial.begin(9600);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");


  server.begin();
  Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());

  // seta pino do transistor para saida

    pinMode(chaveTactilPin, OUTPUT); 


}


// prepare a web page to be send to a client (web browser)
String prepareHtmlPage()
{
  String htmlPage;
  htmlPage.reserve(1024);               // prevent ram fragmentation
  htmlPage = F("HTTP/1.1 200 OK\r\n"
               "Content-Type: text/html\r\n"
               "Connection: close\r\n"  // the connection will be closed after completion of the response
               "Refresh: 5\r\n"         // refresh the page automatically every 5 sec
               "\r\n"
               "<!DOCTYPE HTML>"
               "<html>"
               "Analog input:  ");
  htmlPage += analogRead(A0);
  htmlPage += F("</html>"
                "\r\n");
  return htmlPage;
}


void loop()
{
  WiFiClient client = server.accept();
  // wait for a client (web browser) to connect
  if (client)
  {
    Serial.println("\n[Client connected]");
    while (client.connected())
    {
      // read line by line what the client (web browser) is requesting
      if (client.available())
      {
        String line = client.readStringUntil('\r');
        Serial.println("**********************************************************************************************");
        Serial.println(line);
        Serial.println(BuscarComando(line));
        Serial.println("**********************************************************************************************");

        // wait for end of client's request, that is marked with an empty line
        if (line.length() == 1 && line[0] == '\n')
        {
          client.println(prepareHtmlPage());
          break;
        }
      }
    }

    while (client.available()) {
      // but first, let client finish its request
      // that's diplomatic compliance to protocols
      // (and otherwise some clients may complain, like curl)
      // (that is an example, prefer using a proper webserver library)
      client.read();
    }

    // close the connection:
    client.stop();
    Serial.println("[Client disconnected]");
  }
}

String BuscarComando(String qs) // qs= query string
{
  String qsl = qs; qsl.toLowerCase();
  String retorno="";
  if (qsl.indexOf("comando=ligar") > 0)
  {
    retorno = "LIGAR";
    Ligar();
  } 
  else if (qsl.indexOf("comando=desligar") > 0)
  {
    retorno = "DESLIGAR";
    Desligar();
  }

  return retorno;

}

void Ligar()
{
    digitalWrite(chaveTactilPin, HIGH);
}

void Desligar()
{
    digitalWrite(chaveTactilPin, LOW);

}

