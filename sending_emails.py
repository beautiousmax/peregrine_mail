import smtplib
from email.message import EmailMessage


def send_email(subject, sender, contents, html="", to=(), cc=(), bcc=(), **kwargs):
    """Format and send an email message"""

    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    msg.set_content(contents)

    if html:
        msg.add_alternative(html, subtype='html')

    with smtplib.SMTP('localhost', port=2500) as smtp:
        smtp.send_message(msg)
