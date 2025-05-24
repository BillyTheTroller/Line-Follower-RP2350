#main.py
import wifi
import time
import uasyncio as asyncio
from app import app, get_is_running , set_is_running
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
        if get_is_running():
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
            #left_speed = max(0, min(65535, int(base_speed - correction)))
            #right_speed = max(0, min(65535, int(base_speed + correction)))
            
            # Υπολογισμός αναλογικής μείωσης του εσωτερικού τροχού
            diff = int(abs(correction))

            if correction > 0:
                # στρίβουμε δεξιά: εσωτερικός = αριστερός τροχός
                left_speed  = max(0, base_speed - diff)
                right_speed = base_speed
            elif correction < 0:
                # στρίβουμε αριστερά: εσωτερικός = δεξιός τροχός
                right_speed = max(0, base_speed - diff)
                left_speed  = base_speed
            else:
                # ευθεία
                left_speed = right_speed = base_speed

            # Όρια (0–65535)
            left_speed  = min(left_speed,  65535)
            right_speed = min(right_speed, 65535)


            move_forward(left_speed, right_speed)
            print(f"[PID] error={error:.2f} | L={left_speed} R={right_speed}")
            
            # Έλεγχος για να σταματάει σε 3 άσπρα και 3 μαύρα
            #all_white = all(v < 0.1 for v in normalized)
            all_black = all(v > 0.9 for v in normalized)
            
            if all_black :
                print("Στάση: Όλοι οι αισθητήρες είναι μαύροι/άσπροι! Απενεργοποίηση λειτουργίας.")
                set_is_running(False)
            
        else:
            #print("==> STOPPED")
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



