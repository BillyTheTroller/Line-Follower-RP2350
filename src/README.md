# src/ - Line Follower Core Code

This directory contains the main source code for the line follower robot project.

## Key Components

1. **`main.py`**  
   - Coordinates all modules
   - Runs the 15ms control loop
   - Handles web server startup

2. **`calibration.py`**  
   - Auto-calibrates IR sensors
   - Saves min/max values to `calibration_data.json`

3. **`motor_control.py`**  
   - Controls L298N motor driver
   - Implements PID-based speed adjustment

4. **`pid.py`**  
   - Stores Kp/Ki/Kd parameters
   - Persists settings to `pid_params.json`

## How to Run
```bash
# Ensure dependencies are installed
pip install microdot-asyncio

# Run the main controller
python src/main.py
```

## File Structure
```text
src/
├── main.py           ── Main control loop (entry point)
├── calibration.py    ── IR sensor calibration logic
├── motor_control.py  ── PWM motor driver functions
├── pid.py            ── PID controller implementation
├── motion.py         ── Speed and steering parameters
├── app.py            ── Web Interface and control
├── microdot_asyncio.py ── Ready to Use Library that combines the web interface with the main.py
└── wifi.py           ── Wi-Fi connection handler
