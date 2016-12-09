# -*- coding: utf-8
#  Copyright 2012 Paulo Alem<biggahed@gmail.com>
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

try:
    import json
except ImportError:
    import simplejson as json

BASE_URL = "https://api.temp-io.life"


class WioAPI(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def api(self, path, **kwargs):
        self._make_request(path, **kwargs)

    @gen.engine
    def _make_request(self, path, query=None, method="GET", body=None, callback=None):
        """
        Makes request on `path` in the graph.

        path -- endpoint to the facebook graph api
        query -- A dictionary that becomes a query string to be appended to the path
        method -- GET, POST, etc
        body -- message body
        callback -- function to be called when the async request finishes
        """
        if not query:
            query = {}

        if self.access_token:
            if body is not None:
                body["access_token"] = self.access_token
            else:
                query["access_token"] = self.access_token

        query_string = urllib.urlencode(query) if query else ""
        if method == "GET":
            body = None
        else:
            body = urllib.urlencode(body) if body else ""

        url = BASE_URL + path
        if query_string:
            url += "?" + query_string
        
        print "=====>", url
        print "###### method, body: ", method, body
        
        client = AsyncHTTPClient()
        request = HTTPRequest(url, method=method, body=body)
        response = yield gen.Task(client.fetch, request)

        content_type = response.headers.get('Content-Type')
        print "#### content_type: ", content_type
        print "#### body: ", response.body
        if 'text' in content_type or 'json' in content_type:
            data = json.loads(response.body.decode())
        elif 'image' in content_type:
            data = {
                "data": response.body,
                "mime-type": content_type,
                "url": response.request.url,
            }
        else:
            raise WioAPIError('Maintype was not json, text or image')

        if data and isinstance(data, dict) and data.get("error"):
            raise WioAPIError(data)
        callback(data)


class WioAPIError(Exception):
    def __init__(self, result):
        self.result = result
        try:
            self.type = result["error_code"]
        except:
            self.type = ""

        # OAuth 2.0 Draft 10
        try:
            self.message = result["error_description"]
        except:
            # OAuth 2.0 Draft 00
            try:
                self.message = result["error"]["message"]
            except:
                # REST server style
                try:
                    self.message = result["error_msg"]
                except:
                    self.message = result

        Exception.__init__(self, self.message)
