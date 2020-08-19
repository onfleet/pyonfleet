import requests
import json
import sys
import os
from requests.auth import HTTPBasicAuth
from onfleet.endpoint import Endpoint
from onfleet.error import ValidationError
from onfleet.config import Config

class Onfleet(object):
    # Loading config data
    data = Config.data
    # Look up local authentication JSON if no api_key was passed
    if (os.path.isfile(".auth.json")):
        with open(".auth.json") as json_secret_file:
            secret = json.load(json_secret_file)

    def __init__(self, api_key=None):
        self._session = requests.Session()
        # auth takes api_key and api_secret
        self._session.auth = (api_key if api_key else self.secret["API_KEY"], "")
        self._initialize_resources(self._session)

    def auth_test(self):
        path = self.data["URL"]["base_url"] + self.data["URL"]["version"] + self.data["URL"]["auth_test"]
        response = self._session.get(path)
        return response.json()

    def _initialize_resources(self, session):
        resources = self.data["RESOURCES"]
        # Go through the config module to create endpoints
        for endpoint, http_methods in resources.items():
            setattr(self, endpoint, Endpoint(http_methods, session))
