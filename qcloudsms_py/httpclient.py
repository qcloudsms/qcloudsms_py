#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import re
import json
import sys
import socket

if sys.version_info >= (3,):
    from http import client as httplib
    from urllib import parse as urlparse
else:
    import httplib
    import urlparse


class HTTPRequest(object):

     def __init__(self, url, method="GET", headers=None, body=None):
         """
         :param url: HTTP request URL.
         :param method:  (optiona) HTTP method.
         :param headers: (optional) Dictionary for HTTP request headers.
         :param body: (optional) Dictionary for HTTP request body.
         :param connect_timeout: (optional) HTTP connection timeout.
         :param request_timeout: (optional) HTTP request timeout.
         """
         self.url = url
         self.method = method
         self.headers = headers
         self.body = body


class HTTPResponse(object):

    def __init__(self, request, code, body,
                 headers=None, reason=None):
        """
         :param request: HTTPRequest instance.
         :param code:  HTTP status code.
         :param body: Raw bytes of HTTP response body.
         :param headers: (optional) Dictionary for HTTP response headers.
         :param reason: (optional) HTTP status reason.
         """
        self.request = request
        self.code = code
        self.body = body
        self.headers = headers
        self.reason = reason or httplib.responses.get(code, "Unknown")

    def ok(self):
        if self.code == 200 or self.code == "200":
            return True
        return False

    def json(self):
        if sys.version_info >= (3, ) and sys.version_info < (3, 6):
            return json.loads(self.body.decode("utf-8"),
                              encoding="utf=8")
        return json.loads(self.body, encoding="utf-8")


class HTTPError(Exception):

    def __init__(self, code, reason=None):
        self.code = code
        self.reason = reason or httplib.responses.get(code, "Unknown")
        super(HTTPError, self).__init__(code, reason)

    def __str__(self):
        return "HTTP {}: {}".format(self.code, self.reason)
    __repr__ = __str__


if sys.version_info >= (3,):
    unicode_type = str
else:
    unicode_type = unicode


def utf8(value):
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned
    unchanged. Otherwise it must be a unicode string and is encoded
    as utf8.

    NOTE: This method copy from https://github.com/tornadoweb/tornado and
          copyright belongs to the original author.
    """
    if isinstance(value, (bytes, type(None))):
        return value
    if not isinstance(value, unicode_type):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.encode("utf-8")


class HTTPClientInterface(object):

    def fetch(self, req):
        raise NotImplementedError


class HTTPSimpleClient(HTTPClientInterface):

    PATTERN = "(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*"

    def __init__(self, connect_timeout=60, request_timeout=60,
                 proxy=None):
        self._connect_timeout = connect_timeout
        self._request_timeout = request_timeout
        if isinstance(proxy, (list, tuple)):
            self._proxy = (proxy[0], int(proxy[1]))
        elif isinstance(proxy, (bytes, unicode_type)):
            proxy = utf8(proxy)
            result = re.search(self.__class__.PATTERN, proxy)
            if not result:
                raise ValueError("invalid proxy")
            self._proxy = (
                result.group("host"),
                int(result.group("port")) if result.group("port") else 80
            )
        elif proxy is None:
            self._proxy = None
        else:
            raise ValueError("invalid proxy")

    def fetch(self, req):
        result = urlparse.urlparse(req.url)
        if self._proxy:
            host, port = self._proxy
        else:
            host, port = (result.hostname, result.port)

        if result.scheme == "https":
            conn = httplib.HTTPSConnection(
                host,
                port=port,
                timeout=self._connect_timeout
            )
        else:
            conn = httplib.HTTPConnection(
                host,
                port=port,
                timeout=self._connect_timeout
            )

        if self._proxy:
            conn.set_tunnel(result.hostname, result.port)

        # Send request
        try:
            conn.request(
                req.method,
                "{}?{}".format(result.path, result.query),
                body=utf8(req.body),
                headers=req.headers
            )
            response = conn.getresponse()
            res = HTTPResponse(
                request=req,
                code=response.status,
                body=response.read(),
                headers=dict(response.getheaders()),
                reason=response.reason
            )
        except socket.gaierror:
            # client network error, raise
            raise
        except OSError:
            # client network error, raise
            raise
        finally:
            conn.close()
        return res
