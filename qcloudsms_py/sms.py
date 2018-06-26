#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from qcloudsms_py import util
from qcloudsms_py.httpclient import HTTPRequest


__all__ = [
    "SmsSingleSender",
    "SmsMultiSender",
    "SmsStatusPuller",
    "SmsMobileStatusPuller"
]


class SmsSingleSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://yun.tim.qq.com/v5/tlssmssvr/sendsms"
        self._httpclient = httpclient

    def send(self, sms_type, nationcode, phone_number, msg,
             extend="", ext="", url=None):
        """Send single SMS message.

        :param msg_type: SMS message type, Enum{0: normal SMS, 1: marketing SMS}
        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number: phone number
        :param msg: SMS message content
        :param extend: extend field, default is empty string
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
                "type": int(sms_type),
                "msg": str(msg),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "extend": str(extend),
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)

    def send_with_param(self, nationcode, phone_number, template_id,
                        params, sign="", extend="", ext="", url=None):
        """Send single SMS message with template paramters.

        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param phone_number: phone number
        :param template_id: template id
        :param params: template parameters
        :param sign: Sms user sign
        :param extend: extend field, default is empty string
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
                "sign": str(sign),
                "tpl_id": int(template_id),
                "params": params,
                "sig": util.calculate_signature(
                    self._appkey, rand, now, [phone_number]),
                "time": now,
                "extend": str(extend),
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)



class SmsMultiSender(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2"
        self._httpclient = httpclient

    def send(self, sms_type, nationcode, phone_numbers, msg,
             extend="", ext="", url=None):
        """Send a SMS messages to multiple phones at once.

        :param number: SMS message type, Enum{0: normal SMS, 1: marketing SMS}
        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param phone_numbers: phone number array
        :param msg: SMS message content
        :param extend: extend field, default is empty string
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
                "tel": [{"nationcode": nationcode, "mobile": pn}
                        for pn in phone_numbers],
                "type": int(sms_type),
                "msg": str(msg),
                "sig": util.calculate_signature(
                    self._appkey, rand, now, phone_numbers),
                "time": now,
                "extend": str(extend),
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)

    def send_with_param(self, nationcode, phone_numbers, template_id,
                        params, sign="", extend="", ext="", url=None):
        """
        Send a SMS messages with template parameters to multiple
        phones at once.

        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param phone_numbers: multiple phone numbers
        :param template_id: template id
        :param params: template parameters
        :param sign: Sms user sign
        :param extend: extend field, default is empty string
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
                "tel": [{"nationcode": nationcode, "mobile": pn}
                        for pn in phone_numbers],
                "sign": sign,
                "tpl_id": int(template_id),
                "params": params,
                "sig": util.calculate_signature(
                    self._appkey, rand, now, phone_numbers),
                "time": now,
                "extend": str(extend),
                "ext": str(ext)
            })
        )
        return util.api_request(req, self._httpclient)


class SmsStatusPuller(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._url = "https://yun.tim.qq.com/v5/tlssmssvr/pullstatus"
        self._httpclient = httpclient

    def _pull(self, sms_type, max_num, url=None):
        """Pull SMS message status.

        :param msg_type: SMS message type, Enum{0: normal SMS, 1: marketing SMS}
        :param max_num: maximum number of message status
        :param url: custom url
        """
        rand = util.get_random()
        now = util.get_current_time()
        url = "{}?sdkappid={}&random={}".format(
            url if self._url else url, self._appid, rand)
        req = HTTPRequest(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "sig": util.calculate_signature(
                    self._appkey, rand, now),
                "time": now,
                "type": sms_type,
                "max": max_num
            })
        )
        return util.api_request(req, self._httpclient)

    def pull_callback(self, max_num, url=None):
        """Pull callback SMS messages status.

        :param max_num: maximum number of message status
        :param url: custom url
        """
        return self._pull(0, max_num, url)

    def pull_reply(self, max_num, url=None):
        """Pull reply SMS messages status.

        :param max_num: maximum number of message status
        :param url: custom url
        """
        return self._pull(1, max_num, url)


class SmsMobileStatusPuller(object):

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid;
        self._appkey = appkey;
        self._url = "https://yun.tim.qq.com/v5/tlssmssvr/pullstatus4mobile"
        self._httpclient = httpclient

    def _pull(self, msg_type, nationcode, mobile,
              begin_time, end_time, max_num, url=None):
        """Pull SMS messages status for single mobile.

        :param msg_type: SMS message type, Enum{0: normal SMS, 1: marketing SMS}
        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param mobile: mobile number
        :param begin_time: begin time, unix timestamp
        :param end_time: end time, unix timestamp
        :param max_num: maximum number of message status
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
                "sig": util.calculate_signature(
                    self._appkey, rand, now),
                "type": msg_type,
                "time": now,
                "max": max_num,
                "begin_time": begin_time,
                "end_time": end_time,
                "nationcode": str(nationcode),
                "mobile": str(mobile)
            })
        )
        return util.api_request(req, self._httpclient)

    def pull_callback(self, nationcode, mobile, begin_time,
                      end_time, max_num, url=None):
        """Pull callback SMS message status for single mobile.

        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param mobile: mobile number
        :param begin_time: begin time, unix timestamp
        :param end_time: end time, unix timestamp
        :param max_num: maximum number of message status
        :param url: custom url
        """
        return self._pull(0, nationcode, mobile,
                          begin_time, end_time, max_num, url)

    def pull_reply(self, nationcode, mobile, begin_time,
                   end_time, max_num, url=None):
        """Pull reply SMS message status for single mobile.

        :param nationcode: nation dialing code, e.g. China is 86, USA is 1
        :param mobile: mobile number
        :param begin_time: begin time, unix timestamp
        :param end_time: end time, unix timestamp
        :param max_num: maximum number of message status
        :param url: custom url
        """
        return self._pull(1, nationcode, mobile,
                          begin_time,end_time, max_num, url)
