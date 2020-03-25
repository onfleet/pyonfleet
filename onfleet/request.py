import json
import pkg_resources
import re
import time
import urllib.parse
from onfleet.error import PermissionError, HttpError, RateLimitError, ServiceError
from ratelimit import limits
from backoff import on_exception, expo

RATE_LIMIT = 20
class Request:
    def __init__(self, http_method, path, session):
        self.default_url = "https://onfleet.com/api/v2"
        self.default_headers = {
            "Content-Type": "application/json",
            "User-Agent": "pyonfleet-" + pkg_resources.require("pyonfleet")[0].version
        }
        self.session = session
        self.path = path
        self.http_method = http_method

    @on_exception(expo, RateLimitError, max_tries=8)
    @limits(calls=RATE_LIMIT, period=1)
    def __call__(self, headers=None, queryParams=None, id=None, body=None, **data):
        method = self.http_method
        path_selected = self.url_selector(self.path, id, data)
        url = self.url_joiner(self.default_url, path_selected)
        if (id):
            # TODO: checkIdValidity
            url = self.url_id_replacer(url, id)
        if (len(data) == 1):
            for key, value in data.items():
                url = self.url_endpoint_appender(url, key, value)

        # Check boolean in queryParams and body
        queryParams = self.python_boolean_converter(queryParams) if queryParams else None

        # Headers can be override
        headers = headers or self.default_headers

        # Setting up the HTTP request
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            data=json.dumps(body),
            params=queryParams
        )
        if (response.ok):
            rate_remaining = int(response.headers["X-RateLimit-Remaining"])
            if (rate_remaining < 5):
                time.sleep(1 / rate_remaining)
            return response.status_code if (method == "DELETE" or "complete" in url) else response.json()

        error = json.loads(response.text)
        error_code = error["message"]["error"]
        error_message = error["message"]["message"]
        error_request = error["message"]["request"]
        if (error_code <= 1108 and error_code >= 1100):
            raise PermissionError(error_message, error_code, error_request)
        elif (error_code == 2300):
            raise RateLimitError(error_message, error_code, error_request)
        elif (error_code >= 2500):
            raise ServiceError(error_message, error_code, error_request)
        else:
            raise HttpError(error_message, error_code, error_request)

    @staticmethod
    def url_joiner(url, path):
        return '/'.join(element.strip("/") for element in [url, path])

    @staticmethod
    def url_id_replacer(url, id):
        url = re.sub(r":[a-z]*Id", id, url)
        return url

    @staticmethod
    def url_endpoint_appender(url, key, value):
        if (':param' in url):
            url = re.sub(r":param", key, url)
            url = re.sub(r":[a-z]*Id", value, url)
        else:
            url = re.sub(r":[a-z]*Id", key, url)
            url += '/' + urllib.parse.quote(value)
        return url
    
    @staticmethod
    def url_selector(path, id, data):
        if (isinstance(path, list)):
            get_url = path[0]
            get_by_id_url = path[1]
            if ("shortId" in data):
                path_selected = get_by_id_url
            elif (id is None):
                path_selected = get_url
            else:
                path_selected = get_by_id_url
        else:
            path_selected = path
        return path_selected

    @staticmethod
    def python_boolean_converter(obj):
    # Python Boolean converter - if True and False are passed in, convert to 'true' and 'false'
        for key in obj:
            if (isinstance(obj[key], bool)):
                value = str(obj[key]).lower()
                obj.update({ key: value })
        return obj
