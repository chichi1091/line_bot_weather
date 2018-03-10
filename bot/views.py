# -*- encoding: utf-8 -*-
import os
import json
import requests
import logging
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

logger = logging.getLogger(__name__)


class LineBotView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        logger.info(request.POST)
        
        reply = ""
        for e in request.POST['events']:
            logger.info("{0}".format(e))

            reply_token = e['replyToken']
            message_type = e['message']['type']

            if message_type == 'text':
                text = e['message']['text']
                reply += self.reply_text(reply_token, text)

        return Response(reply)

    def reply_text(self, reply_token, text):
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
