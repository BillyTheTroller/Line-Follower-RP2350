#wifi.py
#Δημιουργία του web server για την διασύνδεση του ρομπότ με το app
import network
import time

# Ρύθμιση του SSID και password του mobile network που ενεργοποιέιται από το mobile hotspot
SSID = 'Jeff'
PASSWORD = 'iuvv1308'

# Σύνδεση του Pico2W με το web app
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('Connected! IP address:', wlan.ifconfig()[0])



