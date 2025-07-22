import subprocess
import os
import time

LOCKER_EXE = "locker.exe"
STOP_FILE = "stop"

def run_locker():
    print("Starting LOCKER app...")
    return subprocess.Popen([LOCKER_EXE])

while True:
    if os.path.exists(STOP_FILE):
        print("Stop file found. Exiting watchdog.")
        break

    process = run_locker()
    process.wait()

    if os.path.exists(STOP_FILE):
        print("LOCKER app ended and stop file created. Watchdog exiting.")
        break

    print("LOCKER app closed unexpectedly! Restarting in 3 seconds...")
    time.sleep(3)
