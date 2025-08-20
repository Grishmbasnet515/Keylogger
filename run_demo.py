import time
from keylogger import Keylogger

if __name__ == "__main__":
    # Report to FILE every 5 seconds
    logger = Keylogger(interval=5, report_method="file")
    logger.start()

    # Simulate some typing
    for ch in ["H", "e", "l", "l", "o", " ", "W", "o", "r", "l", "d", "!"]:
        logger.key_press(ch)
        time.sleep(0.4)

    # Give it a little time to report, then stop
    time.sleep(6)
    logger.stop()
