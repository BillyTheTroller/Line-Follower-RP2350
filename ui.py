# ui.py (νέο αρχείο που θα δημιουργήσουμε στο Pico)

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pico Controller</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        input { margin: 5px; width: 60px; }
        button { margin: 10px; padding: 10px 20px; }
    </style>
</head>
<body>
    <h2>PID Παράμετροι</h2>
    <label>Kp: <input type="number" id="kp" step="0.1"></label><br>
    <label>Ki: <input type="number" id="ki" step="0.1"></label><br>
    <label>Kd: <input type="number" id="kd" step="0.1"></label><br>
    <button onclick="sendPID()">Αποθήκευση PID</button>

    <h2>Έλεγχος</h2>
    <button id="calibrateBtn" onclick="calibrate()">Καλιμπράρισμα</button>
    <button id="startStopBtn" onclick="toggleStart()">Εκκίνηση</button>

    <h2>Κατάσταση</h2>
    <div id="status">Αναμονή...</div>

    <script>
        let started = false;

        function sendPID() {
            const kp = document.getElementById("kp").value;
            const ki = document.getElementById("ki").value;
            const kd = document.getElementById("kd").value;

            fetch(`/set_pid?kp=${kp}&ki=${ki}&kd=${kd}`);
        }

        function calibrate() {
            fetch('/calibrate');
            document.getElementById("status").innerText = "Καλιμπράρισμα σε εξέλιξη...";
        }

        function toggleStart() {
            started = !started;
            fetch(`/toggle_start?state=${started}`);
            document.getElementById("startStopBtn").innerText = started ? "Στάση" : "Εκκίνηση";
            document.getElementById("status").innerText = started ? "Εκκίνηση..." : "Διακοπή...";
        }
    </script>
</body>
</html>
"""

