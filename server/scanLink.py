# import requests
# import json

# # Define the API endpoints and the API key
# scan_endpoint = 'https://developers.checkphish.ai/api/neo/scan'
# status_endpoint = 'https://developers.checkphish.ai/api/neo/scan/status'
# api_key = 'orbm4xsyqjukev9rcj7bw27m4ibtgc1j8i9errli2eosesny25rs18ee86opvitg'

# # Define the URL to scan
# url = 'https://www.checkphish.ai/'

# # Submit URL for scan
# scan_payload = {
#     'apiKey': api_key,
#     'urlInfo': {
#         'url': url
#     }
# }

# scan_response = requests.post(scan_endpoint, json=scan_payload)
# print(scan_response.content.decode('utf-8'))
# # Extract the job ID and timestamp from the response
# job_id = json.loads(scan_response.content.decode('utf-8'))['jobID']
# timestamp = json.loads(scan_response.content.decode('utf-8'))['timestamp']

# # Query scan status and get the results
# status_payload = {
#     'apiKey': api_key,
#     'jobID': job_id,
#     'insights': True
# }

# status_response = requests.post(status_endpoint, json=status_payload)
# print(status_response.content.decode('utf-8'))
# # Extract the results from the response
# results = json.loads(status_response.content.decode('utf-8'))

# # Print the results
# print(results)
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "ksrietcse2021@gmail.com"
receiver_email = "gvishnud10@gmail.com"
password = "Supersecretpassword"
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