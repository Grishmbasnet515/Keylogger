import time
import threading
from datetime import datetime

class Keylogger:
    def __init__(self, interval=10, report_method="file"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""   # store keystrokes here
        self.start_time = datetime.now()

    def key_press(self, event):
        """Simulate a key press (for demo)."""
        self.log += str(event) + " "

    def create_filename(self):
        timestamp = self.start_time.strftime("%Y-%m-%d_%H-%M-%S")
        return f"log_{timestamp}.txt"

    def save_to_file(self):
        filename = self.create_filename()
        with open(filename, "a") as f:
            f.write(self.log + "\n")
        print(f"[+] Saved log to {filename}")
        self.log = ""  # reset after saving

    def report(self):
        if self.report_method == "file":
            self.save_to_file()
        # elif self.report_method == "email":  # future extension
        #     self.send_email()
        # Reschedule next report
        timer = threading.Timer(self.interval, self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        print("[*] Keylogger started (safe demo mode)")
        self.report()
