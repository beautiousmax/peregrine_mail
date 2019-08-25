from flask import Blueprint, request, abort, jsonify, current_app

from peregrine_mail.data.models import Email, email_deliveries_to_dict
from peregrine_mail.data.database import db

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
    db.session.add(email)
    db.session.commit()

    # get id
    db.session.refresh(email)

    # add all the email info to queue
    data['email_id'] = email.id
    current_app.config['EMAIL_QUEUE'].put(data)

    # return the new id
    return jsonify({"email_id": email.id})


@blueprint.route('/', methods=['GET'])
def all_emails():
    """GET returns all email statuses"""
    emails_with_statuses = []

    emails = db.session.query(Email).all()
    for email in emails:
        emails_with_statuses.append(email_deliveries_to_dict(email))
    return jsonify(emails_with_statuses) if emails_with_statuses else "No emails are here"


@blueprint.route('/<email_id>', methods=['GET'])
def specific_email(email_id):

    email = db.session.query(Email).filter(Email.id == email_id).first()
    if not email:
        abort(404)

    return jsonify(email_deliveries_to_dict(email))
