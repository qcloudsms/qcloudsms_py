#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from qcloudsms_py import sms
from qcloudsms_py import voice
from qcloudsms_py import httpclient
from qcloudsms_py.sms import *
from qcloudsms_py.voice import *


# human-readable version number
version = "0.1.3"

# three-tuple for programmatic comparison
version_info = (0, 1, 3)


class QcloudSms(object):

    SMS_CLASSES = set([cls for cls in sms.__all__])
    VOICE_CLASSESS = set([cls for cls in voice.__all__])

    def __init__(self, appid, appkey, httpclient=None):
        self._appid = appid
        self._appkey = appkey
        self._httpclient = httpclient
        self._cache = {}

    def __getattr__(self, name):
        if (name not in self.__class__.SMS_CLASSES and
                name not in self.__class__.VOICE_CLASSESS):
            raise AttributeError("{} is not in {}".format(
                name, self.__class__.__name__))
        if name in self._cache:
            return lambda: self._cache[name]

        if name in self.__class__.SMS_CLASSES:
            cls = getattr(sms, name)
        else:
            cls = getattr(voice, name)
        self._cache[name] = obj = cls(
            self._appid, self._appkey, self._httpclient
        )
        return lambda: obj

    def new(self, name):
        if (name not in self.__class__.SMS_CLASSES and
                name not in self.__class__.VOICE_CLASSESS):
            raise AttributeError("{} is not in {}".format(
                name, self.__class__.__name__))
        if name in self.__class__.SMS_CLASSES:
            return getattr(sms, name)(
                self._appid, self._appkey, self._httpclient
            )
        else:
            return getattr(voice, name)(
                self._appid, self._appkey, self._httpclient
            )
