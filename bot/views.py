# -*- encoding: utf-8 -*-
import os
import logging
import requests

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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

    result = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city=200010")
    if result.status_code != 200:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result.text)
        )

    import json
    json = json.loads(result.text)
    logger.info(json)

    message = ''
    for detail in json['forecasts']:
        message += "{0}({1}):{2} {3}℃/{4}℃ \r\n".format(detail['dateLabel'], detail['date'], detail['telop']
                                                   , detail['temperature']['min'], detail['temperature']['max'])


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
    )

