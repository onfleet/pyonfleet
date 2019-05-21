from onfleet.request import Request

class Endpoint:
    def __init__(self, HttpMethods, Session):
        self.HttpMethods = HttpMethods
        self.Session = Session

        for httpMethod, methodDict in self.HttpMethods.items():
            self._generate_request(httpMethod, methodDict)

    def _generate_request(self, httpMethod, methodDict):
        if (httpMethod):
            http_method = httpMethod
        else:
            raise Exception("Method does not exist")
        # For each method, create the corresponding HTTP request
        for methodName, uri in methodDict.items():
            setattr(self, methodName, Request(http_method, uri, self.Session))    