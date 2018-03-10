# -*- encoding: utf-8 -*-
import os
import json
import requests
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes((AllowAny,))
def callback(request):
    reply = ""
    for e in request.json['events']:
        logger.info("{0}".format(e))

        reply_token = e['replyToken']
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text(reply_token, text)

    return Response(reply)


def reply_text(reply_token, text):
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return text
