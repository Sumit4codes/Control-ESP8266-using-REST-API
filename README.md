# ESP8266 LED Control via Python

This project demonstrates how to control the built-in LED on an ESP8266 module based on a condition evaluated in a Python program. The ESP8266 acts as a web server that listens for HTTP requests to turn the LED on or off.

## Project Overview

- **ESP8266 Code**: Sets up a web server to control the built-in LED based on HTTP GET requests.
- **Python Program**: Sends HTTP requests to the ESP8266 to control the LED based on a condition.

## Components

- ESP8266 module (e.g., NodeMCU, Wemos D1 Mini)
- Python 3.x
- Wi-Fi network

## Requirements

### Hardware

- ESP8266 module
- USB-to-serial adapter (if needed)

### Software

- Arduino IDE
- Python 3.x
- `requests` library for Python

### Libraries

- For ESP8266 (Arduino IDE):
  - `ESP8266WiFi.h`

- For Python:
  - `requests`

## Setup

### ESP8266 Code

1. **Install Arduino IDE**: If not already installed, download and install the [Arduino IDE](https://www.arduino.cc/en/software).

2. **Install ESP8266 Board**: Add ESP8266 support to Arduino IDE:
   - Go to `File` -> `Preferences`
   - Add `http://arduino.esp8266.com/stable/package_esp8266com_index.json` to the "Additional Boards Manager URLs" field
   - Go to `Tools` -> `Board` -> `Boards Manager`
   - Search for `ESP8266` and install the latest version

3. **Upload Code to ESP8266**:
   - Open the `esp8266_led_control.ino` file in Arduino IDE
   - Replace `Your_SSID` and `Your_PASSWORD` with your Wi-Fi credentials
   - Select your ESP8266 board and port from the `Tools` menu
   - Click on `Upload` to upload the code

   ```cpp
   #include <ESP8266WiFi.h>

   const char* ssid = "Your_SSID";
   const char* password = "Your_PASSWORD";

   WiFiServer server(80);

   void setup() {
     Serial.begin(115200);
     pinMode(LED_BUILTIN, OUTPUT);

     WiFi.begin(ssid, password);
     while (WiFi.status() != WL_CONNECTED) {
       delay(1000);
       Serial.println("Connecting to WiFi...");
     }
     Serial.println("Connected to WiFi");

     server.begin();
     Serial.println("Server started");
     Serial.println(WiFi.localIP());
   }

   void loop() {
     WiFiClient client = server.available();
     if (client) {
       Serial.println("New Client Connected");
       String request = client.readStringUntil('\r');
       Serial.println(request);
       client.flush();

       if (request.indexOf("GET /1") != -1) {
         digitalWrite(LED_BUILTIN, LOW);
       } else if (request.indexOf("GET /0") != -1) {
         digitalWrite(LED_BUILTIN, HIGH);
       }

       client.print("HTTP/1.1 200 OK\r\n");
       client.print("Content-Type: text/html\r\n");
       client.print("\r\n");
       client.print("LED state updated");
       client.stop();
       Serial.println("Client Disconnected");
     }
   }
