import json
import re
import time
from urllib import parse

from backoff import on_exception, expo
from ratelimit import limits

from onfleet._meta import __version__
from onfleet.config import API_BASE_URL, RATE_LIMIT
from onfleet.error import HttpError, PermissionError, RateLimitError, ServiceError, ValidationError


class Request:
    '''
    Onfleet API method inside an endpoint (e.g. GET /tasks).
    '''

    def __init__(self, http_method, path, session):
        self.http_method = http_method
        self.path = path
        self.session = session
        self.default_headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'pyonfleet-{__version__}'
        }

    @on_exception(expo, RateLimitError, max_tries=8)
    @limits(calls=RATE_LIMIT, period=1)
    def __call__(self, id=None, body=None, workerId=None, hubId=None, googleApiKey=None, queryParams=None, **extra_data):
        obj_id = id  # TODO(julian): `id` is a reserved name, let's rename it to 'obj_id'
        query_params = queryParams  # TODO(julian): Let's rename `queryParams` to `query_params`

        selected_path = self._path_selector(self.path, obj_id, extra_data)
        url = f'{API_BASE_URL}{selected_path}'

        if obj_id:
            url = self._url_id_setter(url, obj_id)
        if extra_data:
            url = self._url_extra_data_setter(url, extra_data)
        if workerId and hubId:
            body = {
                'path': f'providers/manifest/generate?hubId={hubId}&workerId={workerId}',
                'method': 'GET'
            }
        if googleApiKey:
            self.default_headers['X-Api-Key'] = f'Google {googleApiKey}'

        response = self.session.request(
            method=self.http_method,
            url=url,
            data=json.dumps(body),
            params=self._clean_params(query_params),
            headers=self.default_headers,
        )

        if response.ok:
            rate_remaining = int(response.headers['X-RateLimit-Remaining'])
            if (rate_remaining < 5):
                time.sleep(1 / rate_remaining)
            return response.status_code if (self.http_method == 'DELETE' or 'complete' in url) else response.json()

        error = json.loads(response.text)
        if type(error['message']) is not dict:
            raise HttpError(error.get('message', 'Error'), response.status_code)

        error_message = error['message']['message']
        error_code = error['message']['error']
        error_request = error['message']['request']
        error_cause = error['message'].get('cause')
        exception_args = (error_message, error_code, error_request, error_cause)

        # https://github.com/addyinc/web/blob/master/yerba/config/errors.json

        if 1000 <= error_code <= 1012:  # InvalidContentError
            raise ValidationError(*exception_args)
        elif 1100 <= error_code <= 1112 or error_code == 1300:  # InvalidCredentialsError, ForbiddenError
            raise PermissionError(*exception_args)
        if 2300 <= error_code <= 2301:  # TooManyRequestsError
            raise RateLimitError(*exception_args)
        elif error_code >= 2500:  # InternalError, NotImplementedError, ServiceUnavailableError
            raise ServiceError(*exception_args)

        raise HttpError(*exception_args)

    @staticmethod
    def _path_selector(path, _id, extra_data):
        # Only one path available
        if type(path) is str:
            return path

        # Special case for GET:
        # `path` can be a list of up to 2 paths: to get all resources and to get a specific one.
        # e.g. 'GET /workers' returns all workers and 'GET /workers/123' returns worker with ID=123
        get_url, get_by_id_url = path
        return get_url if not _id and not extra_data else get_by_id_url

    @staticmethod
    def _url_id_setter(url, obj_id):
        # TODO(julian): Check validity of IDs
        # e.g. '/admins/:adminId', 123 --> '/admins/123'
        return re.sub(r':[a-zA-Z]*Id', obj_id, url)

    @staticmethod
    def _url_extra_data_setter(url, extra_data):
        # For now, we only care about just one extra datum
        key, value = next(iter(extra_data.items()))

        # Special case for 'GET /containers':
        # We expect a extra datum like `workers=123`, where...
        # - 'workers' is the type of the entity the container is attached to
        # - '123' the ID of the entity itself
        if ':entityType' in url:
            url = re.sub(r':entityType', key, url)
            url = re.sub(r':entityId', value, url)

        # Special cases for specific look-ups
        elif key in ('shortId', 'name', 'phone'):
            url = re.sub(r':[a-z]*Id', f'{key}/{parse.quote(value)}', url)

        return url

    @staticmethod
    def _clean_params(raw_params):
        # For string, we split comma since the input query parameters are separated by comma
        if type(raw_params) is str:
            params_array = raw_params.split(',')
            params_dict = {}
            # For multiple query parameters, we split by = and set the dictionary
            for param in params_array:
                key, value = param.split('=')
                params_dict[key] = value
            return params_dict

        # For dictionaries, we pass through directly
        elif type(raw_params) is dict:
            return raw_params

