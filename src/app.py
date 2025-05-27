#app.py
# Δημιουργία του web app και όλων των απαραίτητων ρυθμίσεων 
from microdot_asyncio import Microdot, Response
import calibration
import pid
import motion
import uasyncio as asyncio
from calibration import sensors

Response.default_content_type = 'text/html'
app = Microdot()
is_running = False

@app.route('/')
async def index(request):
    params = pid.get_params()
    mparams = motion.get_params()
    html = f"""
    <html><head><meta charset="UTF-8"><title>PID Web UI</title></head><body>
    <h2>Ρυθμίσεις PID</h2>
    <form action="/set" method="post">
        Kp: <input name="kp" value="{params['kp']}"><br>
        Ki: <input name="ki" value="{params['ki']}"><br>
        Kd: <input name="kd" value="{params['kd']}"><br>
        Βασική Ταχύτητα (base_speed): <input name="base_speed" value="{mparams['base_speed']}"><br>
        Πολ/της Διόρθωσης (correction_multiplier): <input name="correction_multiplier" value="{mparams['correction_multiplier']}"><br>
        <button type="submit">Αποθήκευση</button>
    </form>
    <p>Κατάσταση: {'ΤΡΕΧΕΙ' if is_running else 'ΣΤΑΜΑΤΗΜΕΝΟ'}</p>
    <a href="/toggle"><button>Toggle</button></a><br>
    <a href="/calibrate"><button>Καλιμπράρισμα</button></a>
    </body></html>
    """
    return Response(body=html)

@app.route('/toggle')
async def toggle(request):
    print(">>> Toggle πατήθηκε")
    global is_running
    is_running = not is_running
    return f"Κατάσταση: {'ΤΡΕΧΕΙ' if is_running else 'ΣΤΑΜΑΤΗΜΕΝΟ'}"

@app.route('/set', methods=['POST'])
async def set_pid(request):
    try:
        new_params = {
            'kp': float(request.form.get('kp', 0.6)),
            'ki': float(request.form.get('ki', 0)),
            'kd': float(request.form.get('kd', 0))
        }
        pid.update_params(new_params)
        import motor_control
        motor_control.previous_error = 0
        motor_control.integral = 0
        # Motion params
        new_mparams = {
            'base_speed': int(request.form.get('base_speed', 16000)),
            'correction_multiplier': float(request.form.get('correction_multiplier', 10000))
        }
        motion.update_params(new_mparams)
        return f"Νέες τιμές PID: {new_params} και νέες τιμές Motion: {new_mparams}"
    except Exception as e:
        return f"Σφάλμα: {str(e)}"

@app.route('/calibrate') #the whole calibration orchestra
async def calibrate(request):
    try:
        await calibration.calibrate_sensors()
        cal = calibration.get_calibration()
        html = f"""
        <html><body>
        <h3>Καλιμπράρισμα Ολοκληρώθηκε</h3>
        <p>Min: {cal['min']}</p>
        <p>Max: {cal['max']}</p>
        <a href="/">Επιστροφή</a>
        </body></html>
        """
        return Response(body=html)
    except Exception as e:
        return Response(body=f"<h3>Σφάλμα: {e}</h3>")

def start():
    print("Starting async server on 0.0.0.0:80...")
    asyncio.create_task(app.start_server(host="0.0.0.0", port=80))
    asyncio.get_event_loop().run_forever()
    
def get_is_running():
    return is_running





