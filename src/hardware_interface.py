"""
Hardware Interfacing Module: Intel NUC, Arduino UNO & LiDAR Sensor
==================================================================
Project: Personalized Content Delivery Systems (CRTEL Lab / NCSM)
Author: Arafat Ali Mondal

Hardware Topology:
  1. Intel NUC (Edge Processing Core)
  2. 4K USB Camera (Optical Vision Feed)
  3. Arduino UNO (Microcontroller Bridge)
  4. LiDAR Sensor (5V, GND, Data -> Real-Time Visitor Ranging)
  5. Interactive Display & Keyboard / Touch Input
"""

import json
import random
import time
from typing import Optional


class LidarHardwareInterface:
    """
    Manages serial telemetry between Intel NUC and Arduino UNO with LiDAR.
    """

    def __init__(self, port: str = "COM3", baud_rate: int = 115200, mock_mode: bool = False) -> None:
        self.port = port
        self.baud_rate = baud_rate
        self.mock_mode = mock_mode
        self.serial_conn = None

        if not self.mock_mode:
            try:
                import serial
                self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=1.0)
                print(f"[HARDWARE] Connected to Arduino UNO on {self.port} at {self.baud_rate} baud.")
            except Exception as e:
                print(f"[WARN] Hardware serial port {self.port} unavailable ({e}). Falling back to simulation.")
                self.mock_mode = True

    def read_distance(self) -> float:
        """
        Reads visitor distance in centimeters.
        Returns: distance_cm (float) or -1.0 if out of range.
        """
        if self.mock_mode or not self.serial_conn:
            # Simulated realistic visitor distance (120 cm to 280 cm)
            return round(random.uniform(140.0, 220.0), 1)

        try:
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line.startswith("{") and line.endswith("}"):
                data = json.loads(line)
                return float(data.get("distance_cm", -1.0))
        except Exception:
            pass
        return -1.0

    def close(self) -> None:
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("[HARDWARE] Serial connection to Arduino UNO closed.")


def main() -> None:
    print("=== Testing Intel NUC <-> Arduino UNO LiDAR Telemetry ===")
    lidar = LidarHardwareInterface(mock_mode=True)
    try:
        for i in range(5):
            dist = lidar.read_distance()
            print(f"[{i+1}/5] Real-Time Visitor Range: {dist} cm")
            time.sleep(0.5)
    finally:
        lidar.close()


if __name__ == "__main__":
    main()
