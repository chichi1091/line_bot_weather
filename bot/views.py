# -*- encoding: utf-8 -*-
import os
import logging

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from linebot import (
    LineBotApi, WebhookHandler,
    HttpResponse)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
logger = logging.getLogger(__name__)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        try:
            handler.handle(request.body.decode('utf-8'), signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.default()
def default(event):
    logger.info(event)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='サポートされていないテキストメッセージです')
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logger.info(event)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
