import json
import os

import requests

from onfleet.config import API_BASE_URL
from onfleet.endpoint import Endpoint
from onfleet.request import Request


class Onfleet(object):
    '''
    Onfleet API wrapper.
    '''
    _session = requests.Session()

    # Available endpoints.
    # Note that all paths must have '/' only at the beginning, not at the end.

    admins = Endpoint('admins', ('GET', 'POST', 'PUT', 'DELETE'), _session)

    administrators = Endpoint('admins', ('GET', 'POST', 'PUT', 'DELETE'), _session)
    administrators.matchMetadata = Request('POST', '/admins/metadata', _session)

    containers = Endpoint('containers', ('PUT',), _session)
    containers.get = Request('GET', '/containers/:entityType/:entityId', _session)

    destinations = Endpoint('destinations', ('POST'), _session)
    destinations.get = Request('GET', '/destinations/:destinationId', _session)
    destinations.matchMetadata = Request('POST', '/destinations/metadata', _session)

    hubs = Endpoint('hubs', ('GET', 'POST', 'PUT'), _session)

    organization = Endpoint('organization', (), _session)
    organization.get = Request('GET', ['/organization', '/organizations/:orgId'], _session)
    organization.insertTask = Request('PUT', '/containers/organization/:taskId', _session)

    recipients = Endpoint('recipients', ('POST', 'PUT'), _session)
    recipients.get = Request('GET', '/recipients/:recipientId', _session)
    recipients.matchMetadata = Request('POST', '/recipients/metadata', _session)

    tasks = Endpoint('tasks', ('POST', 'PUT', 'DELETE'), _session)
    tasks.get = Request('GET', ['/tasks/all', '/tasks/:taskId'], _session)
    tasks.clone = Request('POST', '/tasks/:taskId/clone', _session)
    tasks.forceComplete = Request('POST', '/tasks/:taskId/complete', _session)
    tasks.batchCreate = Request('POST', '/tasks/batch', _session)
    tasks.autoAssign = Request('POST', '/tasks/autoAssign', _session)
    tasks.matchMetadata = Request('POST', '/tasks/metadata', _session)

    teams = Endpoint('teams', ('POST', 'PUT', 'DELETE'), _session)
    teams.get = Request('GET', ['/teams', '/teams/:orgId'], _session)
    teams.getWorkerEta = Request('GET', '/teams/:teamId/estimate', _session)
    teams.getTasks = Request('GET', '/teams/:teamId/tasks', _session)
    teams.autoDispatch = Request('POST', '/teams/:teamId/dispatch', _session)
    teams.insertTask = Request('PUT', '/containers/teams/:taskId', _session)

    workers = Endpoint('workers', ('POST', 'PUT', 'DELETE'), _session)
    workers.get = Request('GET', ['/workers', '/workers/:workerId'], _session)
    workers.getSchedule = Request('GET', '/workers/:workerId/schedule', _session)
    workers.getByLocation = Request('GET', '/workers/location', _session)
    workers.getTasks = Request('GET', '/workers/:workerId/tasks', _session)
    workers.setSchedule = Request('POST', '/workers/:workerId/schedule', _session)
    workers.matchMetadata = Request('POST', '/workers/metadata', _session)
    workers.insertTask = Request('PUT', '/containers/workers/:taskId', _session)
    workers.getDeliveryManifest = Request('POST', '/integrations/marketplace', _session)

    webhooks = Endpoint('webhooks', ('GET', 'POST', 'DELETE'), _session)

    def __init__(self, api_key=None, custom_headers={}):
        # Looking up local authentication JSON if no api_key was passed
        if not api_key:
            if os.path.isfile(".auth.json"):
                with open(".auth.json") as json_secret_file:
                    local_secret = json.load(json_secret_file)
                    api_key = local_secret.get('API_KEY')
        self._session.auth = (api_key, '')  # Username, password
        # Apply custom headers to all requests if given
        if bool(custom_headers):
            self._session.headers.update(custom_headers)

    def auth_test(self):
        response = self._session.get(f'{API_BASE_URL}/auth/test')
        return response.json()
