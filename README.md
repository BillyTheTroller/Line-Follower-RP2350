# Line-Follower-RP2350
Short and educational line follower project using the Raspberry Pi Pico 2 W platoform

## Overview
This project is a **line-following robot** designed for speed and precision. It uses an **8-channel IR sensor module** to detect a track and adjust movement accordingly. The Raspberry Pi Pico 2 W serves as the microcontroller, processing sensor data and controlling the motors via an **L298N motor driver**. 

## Features
- **Autonomous Line Following**: Uses an 8-channel IR sensor for accurate path tracking.
- **Dual-Motor System**: Two N-20 motors for controlled movement.
- **Power Regulation**: Step-down converter ensures stable voltage supply.
- **Wireless Capability**: Raspberry Pi Pico 2 W allows for remote debugging or expansion.

---

## Hardware List
| Component               | Quantity | Purpose |
|-------------------------|----------|----------|
| **Raspberry Pi Pico 2 W** | 1        | Main microcontroller |
| **3.6V Batteries**       | 2        | Power source for motors and electronics |
| **Battery Case**         | 1        | Holds and connects the batteries |
| **L298 Motor Driver**    | 1        | Controls the motors |
| **N-20 Motors**          | 2        | Provides movement |
| **Step-Down Converter**  | 1        | Regulates voltage from batteries |
| **Wheels**               | 2        | Attached to motors for movement |
| **Ball Caster**          | 1        | Provides balance and smooth turning |
| **Analog IR Sensors**  | 3        | Detects the track for navigation |

---

## Wiring & Circuit Diagram
(You can include a circuit diagram here once finalized.)

### Power Distribution:
- **Batteries (2x3.6V)** → Step-Down Converter → Provides 5V for Raspberry Pi Pico 2 W.
- Motors powered directly via the **L298 motor driver**.

### Motor Control:
- **L298N Motor Driver** receives signals from the **Pico 2 W** to control the N-20 motors.

### Sensor Input:
- The **3 Analog Sensors** send position data to the **Pico 2 W** for line detection.

---

## Software & Code
- Written in **MicroPython**.
- Uses **PWM** for motor speed control.
- Implements **basic PID control** for improved tracking accuracy.

> Full code will be available in the `/code` directory.

---

## Setup & Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/billythetroller/line-follower-rp2350.git
   cd line-follower-rp2350
   ```
2. Flash MicroPython firmware on the Raspberry Pi Pico 2 W.
3. Upload the necessary Python scripts.
4. Assemble the circuit as per the wiring diagram.
5. Power up and start testing!

---

## Contributors
- Vasilis Charmanidis
- Giorgos Karampimperis
- Giannis Diplas
- Apostolis Kefalos

## License
This project is licensed under the **MIT License**.
