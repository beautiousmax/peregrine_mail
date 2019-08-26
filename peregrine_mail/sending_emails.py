import datetime
from email.message import EmailMessage
import logging
import smtplib
import ssl

from peregrine_mail.data.models import Delivery, email_to_dict
from peregrine_mail.data.database import db


logger = logging.getLogger('peregrine')


def send_email(app, email_id, subject, sender, contents, html='', to=(), cc=(), bcc=(), **_):
    """Format and send an email message."""
    db.app = app
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

    logger.info(f'Sending email id {email_id}')
    logger.debug('Mail message:\n' + msg.as_string())
    delivery_attempt = Delivery(email_id=email_id, status='', server_message='')

    try:
        if app.config['SMTP']['ssl']:
            smtp = smtplib.SMTP_SSL(app.config['SMTP']['host'],
                                    port=app.config['SMTP']['port'],
                                    context=ssl.create_default_context(),
                                    timeout=10)
        else:
            smtp = smtplib.SMTP(app.config['SMTP']['host'],
                                port=app.config['SMTP']['port'],
                                timeout=10)
            if app.config['SMTP']['tls']:
                smtp.starttls()
        if app.config['SMTP']['username']:
            smtp.login(user=app.config['SMTP']['username'],
                       password=app.config['SMTP']['password'])
    except (ConnectionError, smtplib.SMTPException) as e:
        delivery_attempt.status = 'unsuccessful'
        delivery_attempt.server_message = str(e)
        logger.warning(f'Could not send email {email_id} due to error "{e}"')
    else:

        try:
            smtp.send_message(msg)
            smtp.quit()
        except smtplib.SMTPException as e:
            delivery_attempt.status = 'unsuccessful'
            delivery_attempt.server_message = str(e)
            logger.warning(f'Could not send email {email_id} due to error "{e}"')
        else:
            delivery_attempt.status = 'successful'
            logger.debug(f'Email {email_id} sent successfully')
    db.session.add(delivery_attempt)
    db.session.commit()


def find_mail_to_send(app, all_emails):
    """
    Find all emails where the latest status is not successful.
    Return email id if number of delivery attempts is less than three and last attempt was >= 10 minutes ago.
    """
    db.app = app
    emails_to_send = []

    for email in all_emails:
        deliveries = db.session.query(Delivery).filter(Delivery.email_id == email.id).order_by(Delivery.attempt).all()

        if deliveries and deliveries[0].status == 'unsuccessful' and len(deliveries) < 3:
            if deliveries[0].attempt + datetime.timedelta(minutes=10) <= datetime.datetime.now():
                emails_to_send.append(email_to_dict(email))
    if emails_to_send:
        logger.debug(f"{len(emails_to_send)} email(s) have been found to re-attempt sending")
    return emails_to_send


def find_mail_to_delete(app, all_emails):
    """ This executes the retention policy to delete old information."""
    db.app = app
    time_offset = datetime.timedelta(days=app.config['PEREGRINE_MAIL']['retain_email_days'])
    now = datetime.datetime.now()
    for email in all_emails:
        if email.created + time_offset <= now:
            logger.debug(f'Deleting email id {email.id}')
            db.session.delete(email)
            db.session.commit()
