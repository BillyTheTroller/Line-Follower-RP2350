import network
import time

SSID = 'gt'
PASSWORD = 'tolis2003'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('Connected! IP address:', wlan.ifconfig()[0])

