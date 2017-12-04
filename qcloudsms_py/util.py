#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import random
import time
import hashlib

from qcloudsms_py.httpclient import HTTPError, http_fetch, utf8


def get_random():
    """Get a random number"""
    return random.randint(100000, 999999)


def get_current_time():
    """Get current time"""
    return int(time.time())


def calculate_signature(appkey, rand, time, phone_numbers=None):
    """Calculate a request signature according to parameters.

    :param appkey: sdk appkey
    :param random: random string
    :param time: unix timestamp time
    :param phone_numbers: phone number array
    """
    raw_text = "appkey={}&random={}&time={}".format(appkey, rand, time)
    if phone_numbers:
        raw_text += "&mobile={}".format(
            ",".join(map(str, phone_numbers)))
    return hashlib.sha256(utf8(raw_text)).hexdigest()


def api_request(req):
    """Make a API request and return response.

    :param req: `qcloudsms_py.httpclient.HTTPRequest` instance
    """
    res = http_fetch(req)
    if not res.ok():
        raise HTTPError(res.code, res.reason)
    return res.json()
