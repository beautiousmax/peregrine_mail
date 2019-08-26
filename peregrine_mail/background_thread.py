import logging
import threading
import time

from peregrine_mail.data.models import Email
from peregrine_mail.data.database import db
from peregrine_mail.sending_emails import send_email, find_mail_to_send, find_mail_to_delete

logger = logging.getLogger('peregrine')


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
        db.app = self.app

        while True:
            # Send NEW emails
            try:
                self.sending_emails_from_queue()
            except Exception as err:
                logger.exception(f'Unexpected error while sending new mail: {err}')

            emails = db.session.query(Email).all()

            # Resend FAILED emails
            try:
                for email in find_mail_to_send(self.app, emails):
                    send_email(self.app, **email)
            except Exception as err:
                logger.exception(f'Unexpected error while finding failed mail to send: {err}')

            # Delete old emails
            try:
                find_mail_to_delete(self.app, emails)
            except Exception as err:
                logger.exception(f'Unexpected error while executing retention policy deletion: {err}')

            time.sleep(self.sleep_time)

    def sending_emails_from_queue(self):
        while not self.email_queue.empty():
            send_email(self.app, **self.email_queue.get())
