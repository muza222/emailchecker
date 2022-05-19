from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import requests
from python_email_validation import AbstractEmailValidation

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

email_subject = "Email test from Flask"
EMAIL_VAL_API_KEY = "5c4da567556b46c780de1698ec424898"

# sanity check route

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify("Email is valid")


@app.route('/validate', methods=['POST'])
def validate():
    try:
        response_object = {'status': 'success'}
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        print(request.json)
        email = request.json["email"]
        if not re.match(regex, email):
            response_object["result_color"] = 'red'
            response_object['message'] = 'Email format is invalid'
            return jsonify(response_object)
        else:
            response_object['message'] = 'Email format is valid'
    except Exception as e:
        print(e)
        return jsonify("Error"), 500

    res = requests.post(
        "https://api.mailgun.net/v3/sandbox6616b3e9684449c6a8011d7f0aa8e8ba.mailgun.org/messages",
        auth=("api", "a2a0653c3e7c42be1b97571d0075a3d7-100b5c8d-4f7bdb9c"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox6616b3e9684449c6a8011d7f0aa8e8ba.mailgun.org>",
              "to": email,
              "subject": "Test from email validator",
              "text": "Email is valid"})
    mailgun = ''
    if res:
        mailgun = "Successfully sended to email using Mailgun (service is not stable)"
    else:
        mailgun = "Cannot to email using Mailgun (service is not stable)"

    AbstractEmailValidation.configure(EMAIL_VAL_API_KEY)
    res = AbstractEmailValidation.verify(email)
    if res:
        response_object["response_data"] = {
            "is_email_valid": "Email is valid (checked by regex)" if res.is_valid_format else "Email is not valid (checked by regex)",
            "is_email_free": "Email is in free email providers list (e.g., Gmail, Yahoo, etc)." if res.is_free_email else "Email is not in free email providers list (e.g., Gmail, Yahoo, etc).",
            "is_email_one_time": "Email was created in disposable email providers (e.g., Mailinator, Yopmail, etc)"
            if res.is_disposable_email else "Email is not in disposable email providers (e.g., Mailinator, Yopmail, etc).",
            'deliverability': res.deliverability,
            'mailgun': mailgun,
        }
        response_object["result_color"] = 'green'
    else:
        response_object["result_color"] = 'red'

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
