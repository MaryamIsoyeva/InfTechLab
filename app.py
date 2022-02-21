# import credentials
import requests
import flask
from flask import Flask, request
app = Flask(__name__)

ACCESS_TOKEN='EABEV2bSVgN8BADQjZBuMxEeesOFQHGhBFCSBydPM9ZBKCn5ZB8CMrsNaAzWPMtrZBleH7UHsWLn8rZAQWDwZBzAC7Qt3JJO1SUcdpZBS1UaTh09btwL1e4ZBCKUvNOSyVXbI6fuWOC6vysvg8bwnjuJ9UZBfNRDmOIDZA3367ZBiZAAIXNNO7LYgNeVv'
VERIFY_TOKEN= 'verify_token'

import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = "6aba030ec0cc4248b856e8c0e5c303dd"
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "eastus"
path = '/translate'
constructed_url = endpoint + path

def translate_func(msg):
    params = {
        'api-version': '3.0',
        'from': "en",
        "to": ['uk']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': msg
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    print(response[0]["translations"][0]["text"])

@app.route('/')
def hello_world():
    return 'Hello, World!'



# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    if verify_token == VERIFY_TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorize.'


@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        translated_text = translate_func(message['text'])
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":translated_text}
            }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+ACCESS_TOKEN, json=request_body).json()
        return response
    return 'ok'

if __name__ == "__main__":
    # translate_func("Good afternoon!")
    app.run(threaded=True, port=5000)