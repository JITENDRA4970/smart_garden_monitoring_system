#include <DHT.h>

#define DHTPIN 2        // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302, AM2321)
#define SOIL_MOISTURE_PIN A0  // Analog pin for soil moisture sensor
#define PUMP_PIN 3      // Digital pin for pump control

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);  // Ensure pump is off at start
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int soilMoisture = analogRead(SOIL_MOISTURE_PIN);

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Send sensor data to Python
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(soilMoisture);

  // Check for commands from Python
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'W') {
      digitalWrite(PUMP_PIN, HIGH);  // Turn on pump
      delay(5000);  // Run for 5 seconds
      digitalWrite(PUMP_PIN, LOW);   // Turn off pump
    }
  }

  delay(180000);  // Wait for 3 minutes (180,000 ms)
}