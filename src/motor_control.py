#motor_control.py
#Συναρτήσεις για την κίνηση του ρομπότ σύμφωνα με την κατεύθυνση των μοτέρ όπως motor_right_forward και υπολογισμός του PID 
from machine import Pin, PWM

# Πινς κατεύθυνσης (IN1–IN4)
motor_left_forward = Pin(9, Pin.OUT)
motor_left_backward = Pin(10, Pin.OUT)
motor_right_forward = Pin(11, Pin.OUT)
motor_right_backward = Pin(12, Pin.OUT)

# PWM Πινς για ταχύτητα (ENA = GP8, ENB = GP13)
pwm_left = PWM(Pin(8))   # ENA
pwm_left.freq(1000)

pwm_right = PWM(Pin(13))  # ENB
pwm_right.freq(1000)

# PID μεταβλητές
previous_error = 0
integral = 0

# Κίνηση μπροστά με ανεξάρτητες ταχύτητες
def move_forward(left_speed, right_speed):
    print(f">> Μπροστά | L={left_speed} R={right_speed}")
    motor_left_forward.on()
    motor_left_backward.off()
    motor_right_forward.on()
    motor_right_backward.off()
    # Μετατροπή 0–1023 → 0–65535
    #left_pwm = int(left_speed * 65535 / 1023)
    #right_pwm = int(right_speed * 65535 / 1023)
    pwm_left.duty_u16(left_speed)
    pwm_right.duty_u16(right_speed)

#Συνάρτηση για πιθανή κίνηση όπισθεν
def move_backward(speed=60000):
    print(">> Πίσω")
    motor_left_forward.off()
    motor_left_backward.on()
    motor_right_forward.off()
    motor_right_backward.on()
    pwm_left.duty_u16(speed)
    pwm_right.duty_u16(speed)

#Συνάρτηση για στροφή αριστερά
def turn_left(speed=60000):
    print(">> Αριστερά")
    motor_left_forward.off()
    motor_left_backward.on()
    motor_right_forward.on()
    motor_right_backward.off()
    pwm_left.duty_u16(speed)
    pwm_right.duty_u16(speed)

#Συνάρτηση για στροφή δεξιά
def turn_right(speed=60000):
    print(">> Δεξιά")
    motor_left_forward.on()
    motor_left_backward.off()
    motor_right_forward.off()
    motor_right_backward.on()
    pwm_left.duty_u16(speed)
    pwm_right.duty_u16(speed)

#Συνάρτηση για να σταματάει
def stop():
    #print(">> Στοπ")
    global previous_error, integral
    previous_error = 0
    integral = 0
    motor_left_forward.off()
    motor_left_backward.off()
    motor_right_forward.off()
    motor_right_backward.off()
    pwm_left.duty_u16(0)
    pwm_right.duty_u16(0)

#Συνάρτηση για τον υπολογισμό του PID
def calculate_pid(error, kp, ki, kd):
    global previous_error, integral

    integral += error # Υπολογίζει το μέθεθος των  errors στην διάρκεια ενός χρονικού διαστήματος και με το ki μπορείς να το μειώσεις
    derivative = error - previous_error # Υπολογιζεί πόσο γρήγορα γίνεται μεταβολή στο error και μπορείς να το ρυθμίσεις με το kd
    output = (kp * error) + (ki * integral) + (kd * derivative) # Συνολικός υπολογισμός 
    previous_error = error #Υπολογισμός προηγούμενου σφάλματος

    return output


