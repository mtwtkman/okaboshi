# -*- coding: utf-8 -*-
import os
import json
import random
import base64
import hashlib
import binascii

import requests
from django.http import JsonResponse
from django.views.generic import View


CHANNEL_ID = os.environ.get('CHANNEL_ID')
MID = os.environ.get('MID')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET', '')

ENDPOINT = 'https://trialbot-api.line.me/v1/events'
FIXIE_URL = os.environ['FIXIE_URL']  # for heroku

def validate_request(sign, data):
    h = hashlib.pbkdf2_hmac('SHA256', data, CHANNEL_SECRET.encode(), 100000)
    if sign == base64.b64encode(binascii.hexlify(h)):
        return True
    return False


def text():
    msgs = [
        '岡星です。',
        '腹のでかい女がいるとうっとおしいので、休ませることにしました。',
        '精神の力をまざまざと感じます。'
    ]
    return {
        'contentType': 1,
        'toType': 1,
        'text': random.choice(msgs)
    }


def traverse(results):
    proxies = {'https': FIXIE_URL}
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': CHANNEL_ID,
        'X-Line-ChannelSecret': CHANNEL_SECRET,
        'X-Line-Trusted-User-With-ACL': MID
    }
    payload = {
        'toChannel': 1383378250,
        'eventType': '138311608800106203',
    }
    for result in results:
        if '岡星' in result['content']['text']:
            payload.update({
                'to': [result['content']['from']],
                'content': text()
            })
            req = requests.post(ENDPOINT,
                                headers=headers,
                                data=json.dumps(payload),
                                proxies=proxies)
        print('request')
        print(req.__dict__)


class OKBSView(View):
    http_method_names = ['get', 'post']

    def get(self, *args, **kwargs):
        return JsonResponse({'okaboshi': 'ryozo'})

    def post(self, request, *args, **kwargs):
        traverse(json.loads(request.body.decode())['result'])
        return JsonResponse({'status': 'post error'})
