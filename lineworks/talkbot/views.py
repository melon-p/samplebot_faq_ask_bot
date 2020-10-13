from django.shortcuts import render

# Create your views here.
from django.views.generic import *
from django.http import HttpResponse

import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import requests
import json
import os

class SendMessage(RedirectView):

    API_ID = "jp1DZgeUkQFax"
    SERVER_ID = "d652934989994dff9396dc1fd4baeac9"
    SERVER_CONSUMER_KEY = "7IYTSRtVBxRUhHfhSF1Q"
    SECRET_KEY_NAME = "private_20201010201635.key"

    def create_tmp_token(self, key_path, server_id):
        
        with open(key_path, "rb") as _file:
            key = _file.read()
            private_key = jwk.JWK.from_pem(key)
            payload = {"iss": server_id}
            token = jwt.generate_jwt(payload, private_key, 'RS256',
                                    datetime.timedelta(minutes=5))
            return token
        return None

    def generate_token(self):

        tmp_token = self.create_tmp_token("talkbot/" + self.SECRET_KEY_NAME, self.SERVER_ID)
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "charset": "UTF-8"
        }
        url = "https://auth.worksmobile.com/b/"+ self.API_ID + "/server/token?grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=" + tmp_token

        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            raise Exception("generate token failed.")

        content = json.loads(response.content)
        token = content.get("access_token", None)
        if token is None:
            raise Exception("response token is None.")

        return token


    def get(self, request, *args, **kwargs):

        url = 'https://apis.worksmobile.com/r/jp1DZgeUkQFax/message/v1/bot/1508250/message/push'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'consumerKey': self.SERVER_CONSUMER_KEY,
            'Authorization': 'Bearer ' + self.generate_token()
        }
        payload = {
            'accountId': 'a.endo@s-store-roumu',
            'content': {
                'type': 'text',
                'text': 'test'
            }
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print(r)
        return HttpResponse('LiNE WORKS に テストメッセージを送信')

    