import threading
from datetime import datetime
from typing import Optional, Dict

try:
    # Local import; make sure mail_sender.py is in the same folder
    from mail_sender import MailSender
except ImportError:
    MailSender = None  # type: ignore


class Keylogger:
    """
    Safe OOP demo of a 'keylogger' architecture:
    - DOES NOT capture real keystrokes.
    - You feed keys via key_press(event).
    - Periodically reports to a file or via (mock) email.
    """

    def __init__(
        self,
        interval: int = 10,
        report_method: str = "file",   # "file" or "email"
        email_config: Optional[Dict] = None,  # {"email": "...", "password": "...", "smtp_server": "...", "port": 587}
        filename: Optional[str] = None,
    ):
        self.interval = int(interval)
        self.report_method = report_method.lower().strip()
        self.log = []
        self.start_time = datetime.now()
        self._timer: Optional[threading.Timer] = None
        self._running = False

        # Filename for file reporting
        self._filename = filename or self.create_filename()

        # Email configuration (optional)
        self.email_config = email_config
        self.mailer = MailSender(**email_config) if (email_config and MailSender) else None

        # Basic validation
        if self.report_method not in {"file", "email"}:
            raise ValueError("report_method must be 'file' or 'email'")

        if self.report_method == "email" and not self.mailer:
            # We still allow running (it will print a friendly message),
            # but warn early so it's clear what's happening.
            print("[!] Email reporting selected but no MailSender available/configured. Will mock-print email content.")

    # ---------------- Core API ---------------- #

    def key_press(self, event) -> None:
        """Collect a simulated keystroke (string-able object)."""
        self.log.append(str(event))

    def create_filename(self) -> str:
        """Create a timestamp-based filename once per session."""
        timestamp = self.start_time.strftime("%Y-%m-%d_%H-%M-%S")
        return f"log_{timestamp}.txt"

    def _drain_log(self) -> str:
        """Get accumulated log as a string and clear buffer."""
        text = " ".join(self.log).strip()
        self.log.clear()
        return text

    def save_to_file(self, text: str) -> None:
        """Append text to the session file."""
        if not text:
            return
        with open(self._filename, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"[+] Saved {len(text)} chars to {self._filename}")

    def send_email_report(self, subject: str, body: str) -> None:
        """Send (or mock-send) the email report."""
        if not body:
            return
        if self.mailer:
            # Real send (uncomment the real send in mail_sender.py)
            self.mailer.send_mail(self.email_config["email"], subject, body)
        else:
            # Mock behavior so the demo is safe
            print("[MOCK EMAIL] To:", self.email_config["email"] if self.email_config else "<not set>")
            print("[MOCK EMAIL] Subject:", subject)
            print("[MOCK EMAIL] Body:")
            print(body)

    def report(self) -> None:
        """Called periodically to report the accumulated log."""
        if not self._running:
            return  # safety if stopped right around the tick

        chunk = self._drain_log()

        if self.report_method == "file":
            self.save_to_file(chunk)
        elif self.report_method == "email":
            subject = "Keylogger Report (SAFE DEMO)"
            self.send_email_report(subject, chunk)

        # Schedule next run
        self._timer = threading.Timer(self.interval, self.report)
        self._timer.daemon = True
        self._timer.start()

    def start(self) -> None:
        """Begin periodic reporting."""
        if self._running:
            return
        self._running = True
        print("[*] Keylogger started (SAFE DEMO). Reporting every", self.interval, "seconds via", self.report_method)
        self.report()

    def stop(self) -> None:
        """Stop periodic reporting."""
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None
        # Final flush if anything remains
        leftover = self._drain_log()
        if leftover:
            if self.report_method == "file":
                self.save_to_file(leftover)
            elif self.report_method == "email":
                self.send_email_report("Keylogger Final Report (SAFE DEMO)", leftover)
        print("[*] Keylogger stopped.")
