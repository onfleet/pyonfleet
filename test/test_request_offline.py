import json
import unittest
from unittest.mock import Mock

from onfleet.error import HttpError, PermissionError, ServiceError, ValidationError
from onfleet.request import Request


def _response(payload, status_code=400, ok=False):
    response = Mock()
    response.ok = ok
    response.text = json.dumps(payload)
    response.status_code = status_code
    response.headers = {'X-RateLimit-Remaining': '100'}
    response.json.return_value = payload
    return response


def _request(http_method, payload, status_code=400, ok=False):
    session = Mock()
    session.request.return_value = _response(payload, status_code, ok)
    return Request(http_method, '/tasks', session)


class TestRequestUrlHelpers(unittest.TestCase):

    def test_path_selector_single_path(self):
        self.assertEqual(Request._path_selector('/tasks', None, {}), '/tasks')

    def test_path_selector_get_all(self):
        paths = ('/workers', '/workers/:workerId')
        self.assertEqual(Request._path_selector(paths, None, {}), '/workers')

    def test_path_selector_get_by_id(self):
        paths = ('/workers', '/workers/:workerId')
        self.assertEqual(Request._path_selector(paths, '123', {}), '/workers/:workerId')

    def test_url_id_setter(self):
        url = Request._url_id_setter('https://onfleet.com/api/v2/admins/:adminId', 'abc123')
        self.assertEqual(url, 'https://onfleet.com/api/v2/admins/abc123')

    def test_url_extra_data_setter_entity(self):
        url = Request._url_extra_data_setter(
            'https://onfleet.com/api/v2/containers/:entityType/:entityId', {'workers': 'w123'})
        self.assertEqual(url, 'https://onfleet.com/api/v2/containers/workers/w123')

    def test_url_extra_data_setter_lookup(self):
        url = Request._url_extra_data_setter(
            'https://onfleet.com/api/v2/tasks/:taskId', {'shortId': '44a5'})
        self.assertEqual(url, 'https://onfleet.com/api/v2/tasks/shortId/44a5')

    def test_clean_params_string(self):
        self.assertEqual(Request._clean_params('from=1,to=2'), {'from': '1', 'to': '2'})

    def test_clean_params_dict_passthrough(self):
        params = {'from': '1'}
        self.assertIs(Request._clean_params(params), params)

    def test_clean_params_none(self):
        self.assertIsNone(Request._clean_params(None))


class TestRequestResponses(unittest.TestCase):

    def test_get_returns_json_body(self):
        payload = {'id': 'abc123'}
        self.assertEqual(_request('GET', payload, status_code=200, ok=True)(), payload)

    def test_delete_returns_status_code(self):
        self.assertEqual(_request('DELETE', {}, status_code=200, ok=True)(), 200)


class TestRequestErrorClassification(unittest.TestCase):

    def _error_payload(self, code):
        return {'message': {'message': 'Boom', 'error': code, 'request': 'req-id'}}

    def test_non_dict_message_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {'message': 'plain text error'})()

    def test_validation_error(self):
        with self.assertRaises(ValidationError):
            _request('GET', self._error_payload(1000))()

    def test_permission_error(self):
        with self.assertRaises(PermissionError):
            _request('GET', self._error_payload(1100))()

    def test_service_error(self):
        with self.assertRaises(ServiceError):
            _request('GET', self._error_payload(2500), status_code=500)()

    def test_unclassified_code_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', self._error_payload(1500))()

    # Regression tests for the fix re-applied from PR #54 (issue #30):
    # payloads with missing optional fields raise the intended exception,
    # not KeyError.
    def test_missing_optional_fields_raise_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {'message': {'message': 'Boom'}})()

    def test_empty_message_dict_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {'message': {}})()

    def test_missing_code_keeps_error_details(self):
        with self.assertRaises(HttpError) as context:
            _request('GET', {'message': {'message': 'Boom'}})()
        self.assertIn('Boom', context.exception.args)

    def test_null_error_code_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {'message': {'message': 'Boom', 'error': None}})()

    def test_string_error_code_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {'message': {'message': 'Boom', 'error': '1000'}})()

    def test_float_error_code_still_classifies(self):
        with self.assertRaises(ValidationError):
            _request('GET', self._error_payload(1000.0))()

    def test_missing_top_level_message_raises_http_error(self):
        with self.assertRaises(HttpError):
            _request('GET', {})()

    def test_non_json_body_raises_http_error(self):
        response = _response({})
        response.text = '<html>502 Bad Gateway</html>'
        session = Mock()
        session.request.return_value = response
        with self.assertRaises(HttpError) as context:
            Request('GET', '/tasks', session)()
        self.assertIn('<html>502 Bad Gateway</html>', context.exception.args)


if (__name__ == '__main__'):
    unittest.main()
