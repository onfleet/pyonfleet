import json
import re
import time

from backoff import on_exception, expo
from ratelimit import limits

from onfleet._meta import __version__
from onfleet.config import API_BASE_URL, RATE_LIMIT
from onfleet.error import PermissionError, HttpError, RateLimitError, ServiceError


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
    def __call__(self, id=None, body=None, queryParams=None, **extra_data):
        obj_id = id  # TODO(julian): `id` is a reserved name, let's rename it to 'obj_id'
        query_params = id  # TODO(julian): Let's rename `queryParams` to `query_params`

        selected_path = self._path_selector(self.path, obj_id)
        url = f'{API_BASE_URL}{selected_path}'

        if obj_id:
            url = self._url_id_setter(url, obj_id)
        if extra_data:
            url = self._url_extra_data_setter(url, extra_data)

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
        try:
            error_code = error['message']['error']
            error_message = error['message']['message']
            error_request = error['message']['request']
            error_cause = error['message'].get('cause')
        except TypeError:
            raise HttpError(error.get('message'), response.status_code)

        if error_code <= 1108 and error_code >= 1100:
            raise PermissionError(error_message, error_code, error_request)
        elif error_code == 2300:
            raise RateLimitError(error_message, error_code, error_request)
        elif error_code >= 2500:
            raise ServiceError(error_message, error_code, error_request)
        raise HttpError(error_message, error_code, error_request, error_cause)

    @staticmethod
    def _path_selector(path, _id):
        # Only one path available
        if type(path) is str:
            return path

        # Special case for GET:
        # `path` can be a list of up to 2 paths: to get all resources and to get a specific one.
        # e.g. 'GET /workers' returns all workers and 'GET /workers/123' returns worker with ID=123
        get_url, get_by_id_url = path
        return get_url if not _id else get_by_id_url

    @staticmethod
    def _url_id_setter(url, obj_id):
        # TODO(julian): Check validity of IDs
        # e.g. '/admins/:adminId', 123 --> '/admins/123'
        return re.sub(r':[a-z]*Id', obj_id, url)

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

        # Special case for 'shortId'
        elif key == 'shortId':
            url = re.sub(r':shortId', f'{key}/{value}', url)

        return url

    @staticmethod
    def _clean_params(raw_params):
        if type(raw_params) is str:
            # 'phones=<phone_number>' --> {'phones': '<phone_number>'}
            key, value = raw_params.split('=')
            return {key: f'{value}'}
