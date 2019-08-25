import threading
import time

from sending_emails import send_email, find_mail_to_send


class Threading:
    """Run emails in the background"""

    def __init__(self, email_queue, app, sleep_time=10):
        self.app = app
        self.email_queue = email_queue
        self.sleep_time = sleep_time
        thread = threading.Thread(target=self.send_emails)
        thread.daemon = True
        thread.start()

    def send_emails(self):
        while True:
            # Send NEW emails
            self.sending_emails_from_queue()

            # Resend FAILED emails
            for email in find_mail_to_send(self.app):
                send_email(self.app, *email)

            time.sleep(self.sleep_time)

    def sending_emails_from_queue(self):
        while not self.email_queue.empty():
            send_email(self.app, *self.email_queue.get())
