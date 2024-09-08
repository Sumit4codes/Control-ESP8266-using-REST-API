#include <ESP8266WiFi.h>

const char* ssid = "you";
const char* password = "sumit@1234";

// Set up a web server on port 80
WiFiServer server(80);

void setup() {
  // Initialize the serial monitor
  Serial.begin(9600);

  // Set the built-in LED pin as output
  pinMode(LED_BUILTIN, OUTPUT);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Start the server
  server.begin();
  Serial.println("Server started");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Listen for incoming clients
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("New Client Connected");
    String request = client.readStringUntil('\r');
    Serial.println(request);
    client.flush();

    // Check the request to see if it contains "GET /1" or "GET /0"
    if (request.indexOf("GET /1") != -1) {
      digitalWrite(LED_BUILTIN, LOW); // Turn on the LED (LOW is ON for the ESP8266)
    } else if (request.indexOf("GET /0") != -1) {
      digitalWrite(LED_BUILTIN, HIGH); // Turn off the LED (HIGH is OFF for the ESP8266)
    }

    // Send a response back to the client
    client.print("HTTP/1.1 200 OK\r\n");
    client.print("Content-Type: text/html\r\n");
    client.print("\r\n");
    client.print("LED state updated");
    client.stop();
    Serial.println("Client Disconnected");
  }
}
