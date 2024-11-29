/*

1. conectar na mesma rede da COISA
1. abrir o navegador: chrome, mozila, ...
2. para LIGAR deve informar no navegador a url: http://<IP da COISA>/comando=ligar
3. para DESLIGAR deve informar no navegador a url: http://<IP da COISA>/comando=ligar

*/

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>


const char* ssid = "nandonet"; 
const char* password = "08111969";

const int chaveTactilPin = D0 ; 


WiFiServer server(80);

// seguro inicio

const char cert_DigiCert_Global_Root_CA [] PROGMEM = R"CERT(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)CERT";


const char* github_host = "meteorologia.negritando.com"; // meteorologia.negritando.com
                           
const uint16_t github_port = 443;

X509List cert(cert_DigiCert_Global_Root_CA);

WiFiClientSecure client;

// seguro fim

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


// seguro inicio


  // Set time via NTP, as required for x.509 validation
  configTime(3 * 3600, 0, "pool.ntp.org", "time.nist.gov");

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));

  // Use WiFiClientSecure class to create TLS connection
  //WiFiClientSecure client;
  Serial.print("Connecting to ");
  Serial.println(github_host);

  Serial.printf("Using certificate: %s\n", cert_DigiCert_Global_Root_CA);
  client.setTrustAnchors(&cert);

  if (!client.connect(github_host, github_port)) {
    Serial.println("Connection failed");
    return;
  }
  else
  {
        Serial.println("Connection sucess");

  }

// seguro fim

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
    MensagemEnviar("motor ligado");
}

void Desligar()
{
    digitalWrite(chaveTactilPin, LOW);
    MensagemEnviar("motor desligado");
}


void MensagemEnviar(String frase)
{

  String url = "/api/clima";
  Serial.print("Requesting URL: ");
  Serial.println(url);

  String output = JsonGerar(frase);

  // client.println(String("POST ") + url +" HTTP/1.1");
  // client.println("Host: " + String(github_host));
  // client.println("Content-Type: application/json" );
  // client.println("Content-Length: " + output.length() );
  // client.println();
  // client.println(output + "\n");

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                 "Host: " + String(github_host) + "\r\n" +
                 //"Connection: close\r\n" +
                 "Content-Type: application/json\r\n" +
                 "Content-Length: " + output.length() + "\r\n" +
                 "\r\n" + // This is the extra CR+LF pair to signify the start of a body
                 output + "\n");  


  Serial.println("----- lendo inicio -------");
  Serial.println(output);
  Serial.println("----- lendo final -------");

  Serial.println("----- lendo inicio -------");
  Serial.println(JsonObter(client));
  Serial.println("----- lendo final -------");

}


String JsonGerar(String frase)
{
  // Allocate the JSON document
  JsonDocument doc;

  // Add values in the document
  doc["id"] = 0;
  doc["nome"] = "ESP32a";
  doc["pressao"] = 56.78D;
  doc["temperatura"] = 67.89D;
  doc["umidade"] = 78.90D;
  doc["situacao"] = frase;

  String out;
  serializeJson(doc, out);

  return out;

}

String JsonObter(BearSSL::WiFiClientSecure cliente)
{
  String desprezado = cliente.readStringUntil('{'); 
  String json = '{' +  cliente.readString(); 
  return json;
}
