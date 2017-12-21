#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from qcloudsms_py.sms import (
    SmsSingleSender, SmsMultiSender,
    SmsStatusPuller, SmsMobileStatusPuller
)
from qcloudsms_py.voice import SmsVoiceVerifyCodeSender, SmsVoicePromptSender


# human-readable version number
version = "0.1.1"

# three-tuple for programmatic comparison
version_info = (0, 1, 1)
