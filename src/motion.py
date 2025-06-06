# motion.py
# Ορίζουμε παραμέτρους όπως ταχύτητα και πολλαπλασιαστή διόρθωσης και τις ρυθμίζουμε από το web interface 
import ujson

# Default motion parameters
motion_params = {
    'base_speed': 16000, #ταχύτητα
    'correction_multiplier': 10000 #πόσο πολύ διορθώνεται το σφάλμα
}

file_path = "motion_params.json"

#Ενημερώνονται οι παράμετροι
def update_params(new_params):
    """
    Ενημερώνει τις τιμές και αποθηκεύει στο flash.
    """
    global motion_params
    motion_params.update(new_params)
    print("Motion params ενημερώθηκαν:", motion_params)
    save_params()

#επιστρέφονται οι τιμές των παραμέτρων
def get_params():
    """
    Επιστρέφει το τρέχον λεξικό με τις παραμέτρους.
    """
    return motion_params

#Αποθηκεύονται οι τιμές των παραμέτρων
def save_params():
    """
    Αποθηκεύει τις motion_params στο JSON.
    """
    try:
        with open(file_path, 'w') as f:
            ujson.dump(motion_params, f)
        print("Motion params αποθηκεύτηκαν στη flash.")
    except Exception as e:
        print("Σφάλμα αποθήκευσης motion params:", e)

#Φορτώνονται οι τιμές των παραμέτρων
def load_params():
    """
    Φορτώνει τις motion_params από το JSON, αν υπάρχει.
    """
    global motion_params
    try:
        with open(file_path, 'r') as f:
            motion_params = ujson.load(f)
        print("Motion params φορτώθηκαν από flash:", motion_params)
    except:
        print("Δεν βρέθηκαν αποθηκευμένα motion params. Χρήση default.")

