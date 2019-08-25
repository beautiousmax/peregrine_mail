from email.message import EmailMessage
import datetime
import smtplib

from data.models import Email, Delivery
from data.database import db


def send_email(email_id, subject, sender, contents, html="", to=(), cc=(), bcc=(), **kwargs):
    """Format and send an email message"""

    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    if cc:
        msg['Cc'] = cc
    if bcc:
        msg['Bcc'] = bcc

    msg.set_content(contents)

    if html:
        msg.add_alternative(html, subtype='html')

    print(msg.as_string())
    delivery_attempt = Delivery(email_id=email_id, status="", server_message="")

    try:
        smtp = smtplib.SMTP('localhost', port=2500)
    except ConnectionError as e:
        delivery_attempt.status = "unsuccessful"
        delivery_attempt.server_message = str(e)
    else:

        try:
            smtp.send_message(msg)
            smtp.quit()
        except smtplib.SMTPException as e:
            delivery_attempt.status = "unsuccessful"
            delivery_attempt.server_message = str(e)
        else:
            delivery_attempt.status = "successful"
    db.session.add(delivery_attempt)
    db.session.commit()


def find_mail_to_send():
    """Find all emails where the latest status is not successful.
    Return email id f number of delivery attempts is less than three and last attempt was >= 10 minutes ago"""
    emails_to_send = []

    emails = db.session.query(Email).all()

    for email in emails:
        deliveries = db.session.query(Delivery).filter(Delivery.email_id == email.id).order_by(Delivery.attempt).all()

        if deliveries[0].status == "unsuccessful" and len(deliveries) < 3:
            if deliveries[0].attempt + datetime.timedelta(minutes=10) >= datetime.datetime.now():
                emails_to_send.append(email.id)

    return emails_to_send
