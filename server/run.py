from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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