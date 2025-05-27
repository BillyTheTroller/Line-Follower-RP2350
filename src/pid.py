# pid.py
# Ορισμός και ρύθμιση παραμέτρων για το PID όπως kp , ki , kd
# Οι συναρτήσεις είναι έτσι ώστε να υπάρχει διασύνδεση με το web app στο background 
import ujson

pid_params = {
    'kp': 5.0,
    'ki': 0.0,
    'kd': 1.0
}

file_path = "pid_params.json"

#Ενημερώνει τις παραμέτρου από το web
def update_params(new_params):
    global pid_params
    pid_params.update(new_params)
    print("PID ενημερώθηκε:", pid_params)
    save_params()
#Επιστρέφει τις παραμέτρους για άλλες εργασίες
def get_params():
    return pid_params
#Αποθηκεύει τις παραμέτρους 
def save_params():
    try:
        with open(file_path, 'w') as f:
            ujson.dump(pid_params, f)
        print("PID αποθηκεύτηκε στη flash.")
    except Exception as e:
        print("Σφάλμα αποθήκευσης PID:", e)
#Φορτώνει τις παραμέτρους 
def load_params():
    global pid_params
    try:
        with open(file_path, 'r') as f:
            pid_params = ujson.load(f)
        print("PID φορτώθηκε από flash:", pid_params)
    except:
        print("Δεν βρέθηκε αποθηκευμένο PID. Χρήση default.")



