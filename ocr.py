# -*- coding=utf-8 -*-
import requests
import json

class AliyunAPIOCRException(Exception):
    pass

class BaseClient(object):

    def __init__(self, app_code=None, app_key=None, app_secret=None):
        super(BaseClient, self).__init__()
        self._app_code=app_code
        self._app_key=app_key
        self._app_secret=app_secret
        self._url=None

    def _prepend_auth_headers(self, headers={}):
        if self._app_code is not None:
            headers['Authorization'] = 'APPCODE %s' % self._app_code
            return headers
        if self._app_key is not None and self._app_secret is not None:
            header["Authorization"] = "acs " + self.profile.access_key_id + ":" + signature_header(header, api_path, client_info, self.profile.access_key_secret)
            return headers
        raise AliyunAPIOCRException("App Code, App Key, App Secret cannot be all empty.")

    def _post(self, payload, url):
        headers = self._prepend_auth_headers(
            {'Content-Type': 'application/json; charset=UTF-8'}
        )
        result = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        return result.json()

class Normal_OCR(BaseClient):

    def ocr(self, image_base64):
        url = "http://tysbgpu.market.alicloudapi.com/api/predict/ocr_general"
        payload = {
            "inputs": [
    {
        "image": {
            "dataType": 50,                         #50表示image的数据类型为字符串
            "dataValue": image_base64      #图片以base64编码的string/oss图片链接
        },
        "configure": {
            "dataType": 50,
            "dataValue": "{\"min_size\" : 10, \"output_prob\" : false}"
        }
    }]
        }
        return self._post(payload, url)

normal_ocr = Normal_OCR(app_code="2265cc1711dd43768da0ae14fb4d5dac")
