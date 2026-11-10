/*
 * Arduino UNO Firmware for LiDAR Distance Telemetry
 * ==================================================
 * Project: Personalized Content Delivery Systems (CRTEL Lab / NCSM)
 * Author: Arafat Ali Mondal
 * 
 * Hardware Connections:
 *   - LiDAR VCC  -> Arduino 5V
 *   - LiDAR GND  -> Arduino GND
 *   - LiDAR Data -> Arduino Digital Pin 3 (PWM / Serial / I2C)
 *   - Arduino USB -> Intel NUC USB Port (Serial 115200 baud)
 */

#define LIDAR_PIN 3

unsigned long pulseWidth = 0;
int distanceCm = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LIDAR_PIN, INPUT);
  Serial.println(F("[SYSTEM_INIT] Arduino UNO LiDAR Interface Online"));
}

void loop() {
  // Read distance pulse from LiDAR sensor
  pulseWidth = pulseIn(LIDAR_PIN, HIGH, 30000); // 30ms timeout

  if (pulseWidth != 0) {
    distanceCm = pulseWidth / 10; // 10 usec = 1 cm calibration
    // Output JSON format telemetry to Intel NUC
    Serial.print(F("{\"distance_cm\": "));
    Serial.print(distanceCm);
    Serial.println(F("}"));
  } else {
    // Sensor reading timeout or out of range
    Serial.println(F("{\"distance_cm\": -1}"));
  }

  delay(50); // 20 Hz telemetry rate
}
