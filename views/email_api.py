from flask import Blueprint, request, abort, jsonify

from data.models import Email, Delivery
from data.database import db_session
from sending_emails import send_email

blueprint = Blueprint('email', __name__, url_prefix='/')


def clean_up_addresses(e):
    """Verify each address has an @"""
    emails = e.strip().split(',')
    if emails == ['']:
        return None
    for email in emails:
        if '@' not in email:
            abort(400, "Email addresses need an @ in them")
    return ','.join(emails)


@blueprint.route('/', methods=['POST'])
def new_email():
    """POST Creates a new email and returns the id"""
    # grab data out of POST message payload
    data = {"contents": "",
            "to": "",
            "sender": "",
            "cc": "",
            "bcc": "",
            "subject": "",
            "attachments": "",
            "html": False}

    body = request.get_json()

    for k in data.keys():
        if body.get(k):
            data[k] = body[k]

    if not data["to"]:
        abort(400, "Addressee is required")

    data["to"] = clean_up_addresses(data["to"])
    data["sender"] = clean_up_addresses(data["sender"])
    data["cc"] = clean_up_addresses(data["cc"])
    data["bcc"] = clean_up_addresses(data["bcc"])

    # add new email to database
    email = Email(**data)

    db_session.add(email)
    db_session.commit()

    # get id
    db_session.refresh(email)

    # add all the email info to queue
    send_email(**data)

    # return the new id
    return jsonify({"email_id": email.id})


@blueprint.route('/', methods=['GET'])
def all_emails():
    """GET returns all email statuses"""
    statuses = {}
    emails = db_session.query(Email).all()
    for email in emails:
        status = db_session.query(Delivery).filter(Delivery.email_id == email.id).order_by(Delivery.attempt).first()
        statuses[email.id] = status
    return jsonify(statuses) if statuses else "No emails are here"


@blueprint.route('/<email_id>')
def specific_email(email_id):
    status = db_session.query(Delivery).filter(Delivery.email_id == email_id).order_by(Delivery.attempt).first()
    return jsonify(status)
