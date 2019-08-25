import datetime
from sqlalchemy import (Column, Integer, Text, ForeignKey, DateTime)
from sqlalchemy.orm import relationship

from data.database import db


class Delivery(db.Model):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('email.id'))
    status = Column(Text)
    server_message = Column(Text)
    attempt = Column(DateTime, default=datetime.datetime.now)


class Email(db.Model):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True)
    deliveries = relationship(Delivery, cascade="all,delete")
    contents = Column(Text)
    to = Column(Text)
    sender = Column(Text)
    cc = Column(Text)
    bcc = Column(Text)
    subject = Column(Text)
    attachments = Column(Text)
    html = Column(Text)
    created = Column(DateTime, default=datetime.datetime.now)


def email_deliveries_to_dict(email):
    e = email_to_dict(email)
    e["delivery_attempts"] = []
    status = db.session.query(Delivery).filter(Delivery.email_id == email.id).order_by(Delivery.attempt).all()
    for attempt in status:
        s = {"status": attempt.status,
             "server_message": attempt.server_message,
             "attempt": attempt.attempt}
        e['delivery_attempts'].append(s)

    return e


def email_to_dict(email):
    e = {"email_id": email.id,
         "contents": email.contents,
         "to": email.to,
         "sender": email.sender,
         "cc": email.cc,
         "bcc": email.bcc,
         "subject": email.subject,
         "attachments": email.attachments,
         "html": email.html,
         "created": email.created}
    return e
