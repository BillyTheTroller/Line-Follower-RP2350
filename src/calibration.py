# calibration.py
# Πέρνουν τιμές οι αισθητήρες από 0 μέχρι 65535 διότι είναι αναλογικοί 
# Για να ξεχωρίζει το ρομπότ το μαύρο από τα άλλα χρώματα πάντα ανάλογα με τον φωτισμό
import ujson
from machine import ADC, Pin
import time  # Χρησιμοποιούμε την βιβλιοθήκη time για χρονισμό
import uasyncio as asyncio

# Σύνδεση αισθητήρων
sensors = [ADC(Pin(26)), ADC(Pin(27)), ADC(Pin(28))]

# Ορισμός αρχείου για αποθήκευση calibration
calibration_file = 'calibration_data.json'

# Αρχικές τιμές calibration
calibration = {
    'min': [65535, 65535, 65535],
    'max': [0, 0, 0]
}

# Εκκίνηση καλιμπραρίσματος
async def calibrate_sensors():
    calibration['min'] = [65535, 65535, 65535]
    calibration['max'] = [0, 0, 0]
    print("Ξεκινά καλιμπράρισμα...")

    duration_ms = 10000  # Διάρκεια καλιμπραρίσματος σε ms
    interval_ms = 10    # Διάστημα αναγνώρισης κάθε τιμής (σε ms)
    start = time.ticks_ms()  # Χρονισμός καλιμπραρίσματος με time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
        for i, sensor in enumerate(sensors):
            value = sensor.read_u16()  # Ανάγνωση τιμής από τον αισθητήρα
            if value < calibration['min'][i]:
                calibration['min'][i] = value
            if value > calibration['max'][i]:
                calibration['max'][i] = value
        await asyncio.sleep_ms(interval_ms)

    print("Καλιμπράρισμα ολοκληρώθηκε.")
    print("Min:", calibration['min'])
    print("Max:", calibration['max'])

    save_calibration()  # Αποθήκευση των αποτελεσμάτων σε αρχείο

# Αποθήκευση calibration σε αρχείο
def save_calibration():
    try:
        with open(calibration_file, 'w') as f:
            ujson.dump(calibration, f)
        print("Αποθηκεύτηκε το calibration.")
    except Exception as e:
        print("Σφάλμα αποθήκευσης:", e)

# Φόρτωση calibration από αρχείο
def load_calibration():
    global calibration
    try:
        with open(calibration_file, 'r') as f:
            calibration = ujson.load(f)
        print("Φορτώθηκαν calibration:", calibration)
    except Exception as e:
        print("Δεν βρέθηκε αρχείο calibration ή προέκυψε σφάλμα:", e)

# Επιστροφή calibration
def get_calibration():
    return calibration


