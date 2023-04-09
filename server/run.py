from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import smtplib
import ssl

SENDGRID_API_KEY = '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'


app = Flask(__name__)
CORS(app)


@app.route('/report', methods=['POST'])
def report():
    # Get the URL from the POST request data
    url = request.json['id']
    print("This is the URL:", url)

    # Analyze the URL and determine suspicious IDs
    suspicious_ids = analyze_url(url)

    # Return the suspicious IDs as a JSON response
    response_data = {'suspicious_ids': suspicious_ids}
    return jsonify(response_data)


def analyze_url(url):
    # TODO: Implement URL analysis code here
    suspicious_ids = ["vishnu", "id1", "id2", "id3"]
    # print("Sending email notification...")
    # message = "The following suspicious IDs were found: {}".format(suspicious_ids)
    # send_email(message)
    # Return the suspicious IDs
    return suspicious_ids


def analyze_data(data):
    url = "https://sead.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": "320e403e955c478e824e69ede8f06eda",
        "Apim-Request-Id": "4ffcac1c-b2fc-48ba-bd6d-b69d9942995a",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "PARTICIPANT_ID_HERE",
                "text": data,
                "modality": "text",
                "language": "en",
                "participantId": "PARTICIPANT_ID_HERE"
            }
        },
        "parameters": {
            "projectName": "seader",
            "verbose": True,
            "deploymentName": "seader",
            "stringIndexType": "TextElement_V8"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    answer = response.json()
    # print(answer)
    print(answer['result']['prediction']['topIntent'])


def send_email():
    port = 587  # For starttls


    smtp_server = "smtp.gmail.com"
    sender_email = "ksrietcse2021@gmail.com"
    receiver_email = "gvishnud10@gmail.com"
    password = "eznscahkroajykpn"
    message = """\
    Subject: Unusual activity detected

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        
        server.sendmail(sender_email, receiver_email, message)

test_data = "your pic is nice bro"
analyze_data(test_data)
send_email()


# def send_email(body):
# message = Mail(
#     from_email='gvishnu.roboenge@gmail.com',
#     to_emails='gvishnud10@gmail.com',
#     subject='Unusual activity detected',
#     html_content=body)
# try:
#     sg = SendGridAPIClient(SENDGRID_API_KEY)
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
