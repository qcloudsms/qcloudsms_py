#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from qcloudsms_py import util
from qcloudsms_py.httpclient import HTTPRequest


class SmsVoicePromptSender(object):

    def __init__(self, appid, appkey, url=None, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://yun.tim.qq.com/v5/tlsvoicesvr/sendvoiceprompt"

    def send(self, nation_code, phone_number, prompttype, msg, playtimes=2, ext=""):
        """Send a voice prompt message.

        :param naction_code: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number: phone number
        :param prompttype: voice prompt type, currently value is 2
        :param msg: voice prompt message
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body={
                "tel": {
                    "nationcode": str(nation_code),
                    "mobile": str(phone_number)
                },
                "prompttype": prompttype,
                "promptfile": str(msg),
                "playtimes": int(playtimes),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "ext": str(ext)
            },
            connect_timeout=60,
            request_timeout=60
        )
        return util.api_request(req)


class SmsVoiceVerifyCodeSender(object):

    def __init__(self, appid, appkey):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://yun.tim.qq.com/v5/tlsvoicesvr/sendvoice";

    def send(self, nation_code, phone_number, msg,
             playtimes=2, ext=""):
        """Send a voice verify code message.

        :param nation_code: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number:  phone number
        :param msg: voice verify code message
        :param playtimes: playtimes, optional, max is 3, default is 2
        :param ext: ext field, content will be returned by server as it is
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            self._url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body={
                "tel": {
                    "nationcode": str(nation_code),
                    "mobile": str(phone_number)
                },
                "msg": "msg",
                "playtimes": int(playtimes),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "ext": str(ext)
            },
            connect_timeout=60,
            request_timeout=60
        )
        return util.api_request(req)
