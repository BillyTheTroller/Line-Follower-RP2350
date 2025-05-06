#main.py
import wifi
import time
import uasyncio as asyncio
from app import app, get_is_running
from calibration import sensors, load_calibration, get_calibration
from motor_control import calculate_pid, move_forward, stop
import pid
import motion
import calibration

# Παγκόσμια μεταβλητή calibration
cal_data = {}

# PID control + αισθητήρες
async def control_loop():
    
    while True:
        sensor_values = ir_sensors.read() #possible bug but attempt 1 nonetheless
        if all(value == 1 for value in sensor_values): #black=1 => if all black then the line follower stops moving
            stop()
            continue #end of modified code 
        get_is_running():
            #print("==> STARTING")
            
            m = motion.get_params()
            base_speed = m['base_speed']
            multiplier = m['correction_multiplier']
            
            values = [s.read_u16() for s in sensors]

            # Κανονικοποίηση
            
            cal = calibration.get_calibration()    # always fresh
            normalized = [
               (v - cal['min'][i]) / max(1, (cal['max'][i] - cal['min'][i]))
               for i, v in enumerate(values)
            ]

            # Υπολογισμός σφάλματος
            error = normalized[0] - normalized[2]

            # PID
            p = pid.get_params()
            raw = calculate_pid(error, p['kp'], p['ki'], p['kd'])
            correction = multiplier * raw

            # Ταχύτητες με περιορισμό
            left_speed = max(0, min(65535, int(base_speed - correction)))
            right_speed = max(0, min(65535, int(base_speed + correction)))

            move_forward(left_speed, right_speed)
            print(f"[PID] error={error:.2f} | L={left_speed} R={right_speed}")
        else:
            #print("==> STOPPED")
            stop()

        await asyncio.sleep_ms(5)

# Κύρια συνάρτηση
async def main():
    print("Σύνδεση WiFi...")
    wifi.connect()

    print("Φόρτωση calibration...")
    load_calibration()
    global cal_data
    cal_data = get_calibration()

    print("Φόρτωση PID...")
    pid.load_params()
    
    print("Φόρτωση Motion params...")
    motion.load_params()

    print("Εκκίνηση control loop...")
    asyncio.create_task(control_loop())

    print("Starting async server on 0.0.0.0:80...")
    await app.start_server(host="0.0.0.0", port=80)

# Τρέξιμο
asyncio.run(main())

