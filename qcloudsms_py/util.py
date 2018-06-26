#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import random
import time
import hashlib
import json

from qcloudsms_py.httpclient import HTTPError, HTTPSimpleClient, utf8


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


def calculate_auth(appkey, rand, time, file_sha1sum):
    """Calculate a auth signature for uploading voice file.

    :param appkey: sdk appkey
    :param random: random string
    :param time: unix timestamp time
    :param file_sha1sum: voice file sha1 sum
    """
    raw_text = "appkey={}&random={}&time={}&content-sha1={}".format(
        appkey, rand, time, file_sha1sum
    )
    return hashlib.sha256(utf8(raw_text)).hexdigest()


def sha1sum(content):
    return hashlib.sha1(utf8(content)).hexdigest()


_http_simple_client = HTTPSimpleClient()


def api_request(req, httpclient=None):
    """Make a API request and return response.

    :param req: `qcloudsms_py.httpclient.HTTPRequest` instance
    :param httpclient: `qcloudsms_py.httpclient.HTTPClientInterface` instance
    """
    if httpclient:
        res = httpclient.fetch(req)
    else:
        res = _http_simple_client.fetch(req)
    if not res.ok():
        raise HTTPError(res.code, res.reason)
    return res.json()
