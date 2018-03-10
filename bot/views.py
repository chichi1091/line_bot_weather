# -*- encoding: utf-8 -*-
import json
from linebot import HttpResponse
import requests

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'ENTER YOUR Channel Access Token'
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}


def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        reply_token = e['replyToken']
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text(reply_token, text)

    return HttpResponse(reply)


def reply_text(reply_token, text):
    payload = {
        "replyToken":reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return text
