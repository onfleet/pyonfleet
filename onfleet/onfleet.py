import requests
import json
import sys
import os
from requests.auth import HTTPBasicAuth
from onfleet.endpoint import Endpoint
from onfleet.error import ValidationError

class Onfleet(object):
    with open(os.path.join(sys.prefix, "config/config.json")) as json_data_file:
        data = json.load(json_data_file)
    if (os.path.isfile(".auth.json")):
        with open(".auth.json") as json_secret_file:
            secret = json.load(json_secret_file)

    def __init__(self, api_key=None):
        self._session = requests.Session()
        self._session.auth = (api_key if api_key else self.secret["API_KEY"], "") # auth takes api_key and api_secret
        self._initialize_resources(self._session)

    def auth_test(self):
        path = self.data["URL"]["base_url"] + self.data["URL"]["version"] + self.data["URL"]["auth_test"]
        response = self._session.get(path)
        return response.json()

    def _initialize_resources(self, session):
        resources = self.data["RESOURCES"]
        # Go through the config.json file to create endpoints
        for endpoint, http_methods in resources.items():
            setattr(self, endpoint, Endpoint(http_methods, session))

def verify_webhook(header, body, secret):
    """Verifies that the webhook originated from Onfleet.

    Args: 
        header: can be the full headers in dictionary-like format from the request, or the value of the X-Onfleet-Signature header
        body: should be the full body of the POST request in raw bytes, *not* the parsed JSON object
        secret: the value of the webhook secret from the Onfleet dashboard, in hexadecimal format
    Returns:
        True for verified, False for not verified"""

    import hashlib, hmac, binascii
    if isinstance(header, bytes):
        check_against = header
    elif isinstance(header, str):
        check_against = header.encode('utf8')
    elif hasattr(header, 'get') and callable(header.get) and header.get("X-Onfleet-Signature") is not None:
        check_against = header.get("X-Onfleet-Signature")
    else:
        raise ValueError("header must be bytes, string, or mapping type")
    return hmac.new(binascii.a2b_hex(secret), body, 'sha512').hexdigest() == check_against