#pid.py
import ujson

pid_params = {
    'kp': 5.0,
    'ki': 0.0,
    'kd': 1.0
}

file_path = "pid_params.json"

def update_params(new_params):
    global pid_params
    pid_params.update(new_params)
    print("PID ενημερώθηκε:", pid_params)
    save_params()

def get_params():
    return pid_params

def save_params():
    try:
        with open(file_path, 'w') as f:
            ujson.dump(pid_params, f)
        print("PID αποθηκεύτηκε στη flash.")
    except Exception as e:
        print("Σφάλμα αποθήκευσης PID:", e)

def load_params():
    global pid_params
    try:
        with open(file_path, 'r') as f:
            pid_params = ujson.load(f)
        print("PID φορτώθηκε από flash:", pid_params)
    except:
        print("Δεν βρέθηκε αποθηκευμένο PID. Χρήση default.")



