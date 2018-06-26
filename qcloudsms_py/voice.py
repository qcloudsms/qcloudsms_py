#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from qcloudsms_py import util
from qcloudsms_py.httpclient import HTTPRequest


__all__ = [
    "SmsVoiceVerifyCodeSender",
    "SmsVoicePromptSender",
    "PromptVoiceSender",
    "CodeVoiceSender",
    "TtsVoiceSender",
    "FileVoiceSender",
    "VoiceFileUploader"
]


class PromptVoiceSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://cloud.tim.qq.com/v5/tlsvoicesvr/sendvoiceprompt"
        self._httpclient = httpclient

    def send(self, nationcode, phone_number, prompttype,
             msg, playtimes=2, ext="", url=None):
        """Send a voice prompt message.

        :param naction_code: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number: phone number
        :param prompttype: voice prompt type, currently value is 2
        :param msg: voice prompt message
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        :param url: custom url
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            url if url else self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "tel": {
                    "nationcode": str(nationcode),
                    "mobile": str(phone_number)
                },
                "prompttype": prompttype,
                "promptfile": str(msg),
                "playtimes": int(playtimes),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)


# For compatibility with old API
SmsVoicePromptSender = PromptVoiceSender


class CodeVoiceSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://cloud.tim.qq.com/v5/tlsvoicesvr/sendcvoice"
        self._httpclient = httpclient

    def send(self, nationcode, phone_number, msg,
             playtimes=2, ext="", url=None):
        """Send code voice.

        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number:  phone number
        :param msg: voice verify code message
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        :param url: custom url
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            url if url else self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "tel": {
                    "nationcode": str(nationcode),
                    "mobile": str(phone_number)
                },
                "msg": msg,
                "playtimes": int(playtimes),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)

# For compatibility with old API
SmsVoiceVerifyCodeSender = CodeVoiceSender


class TtsVoiceSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://cloud.tim.qq.com/v5/tlsvoicesvr/sendtvoice"
        self._httpclient = httpclient

    def send(self, template_id, params, phone_number,
             nationcode="86", playtimes=2, ext="", url=None):
        """Send tts voice.

        :param template_id: template id
        :param params: template parameters
        :param phone_number: phone number
        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        :param url: custom url
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            url if url else self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "tel": {
                    "nationcode": str(nationcode),
                    "mobile": phone_number
                },
                "tpl_id": int(template_id),
                "params": params,
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "playtimes": playtimes,
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)


class FileVoiceSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://cloud.tim.qq.com/v5/tlsvoicesvr/sendfvoice"
        self._httpclient = httpclient

    def send(self, fid, phone_number, nationcode="86",
             playtimes=2, ext="", url=None):
        """Send file voice.

        :param fid: voice file fid
        :param phone_number: phone number
        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        :param url: custom url
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            url if url else self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "tel": {
                    "nationcode": str(nationcode),
                    "mobile": phone_number
                },
                "fid": fid,
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "playtimes": playtimes,
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)


class VoiceFileUploader(object):

    CONTENT_TYPES = {
        "wav": "audio/wav",
        "mp3": "audio/mpeg"
    }

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://cloud.tim.qq.com/v5/tlsvoicesvr/uploadvoicefile"
        self._httpclient = httpclient

    def upload(self, file_content, content_type="mp3", url=None):
        """Upload voice file.

        :param file_content: voice file content
        :param content_type: voice file content type
        :param url: custom url
        """
        if content_type not in self.__class__.CONTENT_TYPES:
            raise ValueError("invalid content")
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}&time={}".format(
            url if url else self._url, self._appid, rand, now)
        file_sha1sum = util.sha1sum(file_content)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={
                "Content-Type": self.__class__.CONTENT_TYPES[content_type],
                "x-content-sha1": file_sha1sum,
                "Authorization": util.calculate_auth(
                    self._appkey, rand, now, file_sha1sum
                )
            },
            body=file_content
        )
        return util.api_request(req, self._httpclient)
