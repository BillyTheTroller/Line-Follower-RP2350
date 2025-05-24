#main.py
import wifi
import time
import uasyncio as asyncio
from app import app, get_is_running , set_is_running
from calibration import sensors, load_calibration, get_calibration
from motor_control import calculate_pid, move_forward, stop , turn_right , turn_left
import pid
import motion
import calibration

# Παγκόσμια μεταβλητή calibration
cal_data = {}

# PID control + αισθητήρες
async def control_loop():
    while True:
        if get_is_running():
            m = motion.get_params()
            base_speed = m['base_speed']
            multiplier = m['correction_multiplier']
            
            values = [s.read_u16() for s in sensors]
            cal = calibration.get_calibration()
            normalized = [
               (v - cal['min'][i]) / max(1, (cal['max'][i] - cal['min'][i]))
               for i, v in enumerate(values)
            ]

            error = normalized[0] - normalized[2]
            
            # Detect sharp turns (when error exceeds threshold)
            sharp_turn_threshold = 0.6  # Adjust this value based on your needs
            is_sharp_turn = abs(error) > sharp_turn_threshold
            
            if is_sharp_turn:
                # Tank steering for sharp turns
                if error > 0:  # Sharp right turn
                    turn_left(base_speed)
                    print(f"[SHARP RIGHT] error={error:.2f}")
                else:  # Sharp left turn
                    turn_right(base_speed)
                    print(f"[SHARP LEFT] error={error:.2f}")
            else:
                # Normal PID control for gentle turns
                p = pid.get_params()
                raw = calculate_pid(error, p['kp'], p['ki'], p['kd'])
                correction = multiplier * raw
                
                diff = int(abs(correction))
                if correction > 0:
                    left_speed = max(0, base_speed - diff)
                    right_speed = base_speed
                elif correction < 0:
                    right_speed = max(0, base_speed - diff)
                    left_speed = base_speed
                else:
                    left_speed = right_speed = base_speed

                left_speed = min(left_speed, 65535)
                right_speed = min(right_speed, 65535)
                move_forward(left_speed, right_speed)
                print(f"[PID] error={error:.2f} | L={left_speed} R={right_speed}")
            
            # Check for all black/white
            all_black = all(v > 0.9 for v in normalized)
            if all_black:
                print("Στάση: Όλοι οι αισθητήρες είναι μαύροι/άσπροι! Απενεργοποίηση λειτουργίας.")
                set_is_running(False)
        else:
            stop()
        await asyncio.sleep_ms(15)

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



