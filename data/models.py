import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Text, ForeignKey, DateTime)


Base = declarative_base()


class Email(Base):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True)
    contents = Column(Text)
    to = Column(Text)
    sender = Column(Text)
    cc = Column(Text)
    bcc = Column(Text)
    subject = Column(Text)
    attachments = Column(Text)
    html = Column(Text)
    created = Column(DateTime, default=datetime.datetime.now)


class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('email.id'))
    status = Column(Text)
    server_message = Column(Text)
    attempt = Column(DateTime, default=datetime.datetime.now)
