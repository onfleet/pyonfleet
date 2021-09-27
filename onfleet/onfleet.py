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

    # Available endpoints

    admins = Endpoint('admins', ('GET', 'POST', 'PUT', 'DELETE'), _session)

    administrators = Endpoint('admins', ('GET', 'POST', 'PUT', 'DELETE'), _session)
    administrators.matchMetadata = Request('POST', '/admins/metadata', _session)

    containers = Endpoint('containers', ('PUT',), _session)
    containers.get = Request('GET', '/containers/:param/:containerId', _session)

    destinations = Endpoint('destinations', ('GET', 'POST'), _session)
    destinations.matchMetadata = Request('POST', '/destinations/metadata', _session)

    hubs = Endpoint('hubs', ('GET', 'POST', 'PUT'), _session)

    organization = Endpoint('organization', (), _session)
    organization.get = Request('GET', ['/organization', '/organizations/:orgId'], _session)
    organization.insertTask = Request('PUT', '/containers/organization/:orgId', _session)

    recipients = Endpoint('recipients', ('GET', 'POST', 'PUT'), _session)
    recipients.matchMetadata = Request('POST', '/recipients/metadata', _session)

    recipients = Endpoint('recipients', ('POST', 'PUT', 'DELETE'), _session)
    recipients.get = Request('GET', ['/tasks/all', '/tasks/:taskId'], _session)
    recipients.clone = Request('POST', '/tasks/:taskId/clone', _session)
    recipients.forceComplete = Request('POST', '/tasks/:taskId/complete', _session)
    recipients.batchCreate = Request('POST', '/tasks/batch', _session)
    recipients.autoAssign = Request('POST', '/tasks/autoAssign', _session)
    recipients.matchMetadata = Request('POST', '/tasks/metadata', _session)

    teams = Endpoint('teams', ('POST', 'PUT', 'DELETE'), _session)
    teams.get = Request('GET', ['/teams', '/teams/:orgId'], _session)
    teams.getWorkerEta = Request('GET', '/teams/:teamId/estimate', _session)
    teams.autoDispatch = Request('POST', '/teams/:teamId/dispatch', _session)
    teams.insertTask = Request('PUT', '/containers/teams/:teamId', _session)

    workers = Endpoint('workers', ('POST', 'PUT', 'DELETE'), _session)
    workers.get = Request('GET', ['/workers', '/workers/:workerId'], _session)
    workers.getSchedule = Request('GET', '/workers/:workerId/schedule', _session)
    workers.getByLocation = Request('GET', '/workers/location', _session)
    workers.setSchedule = Request('POST', '/workers/:workerId/schedule', _session)
    workers.matchMetadata = Request('POST', '/workers/metadata', _session)
    workers.insertTask = Request('PUT', '/containers/workers/:workerId', _session)

    webhooks = Endpoint('webhooks', ('GET', 'POST', 'DELETE'), _session)

    def __init__(self, api_key=None):
        if api_key:
            self._session.auth = api_key
        else:
            local_secret = {}
            # Look up local authentication JSON if no api_key was passed
            if os.path.isfile(".auth.json"):
                with open(".auth.json") as json_secret_file:
                    local_secret = json.load(json_secret_file)
            self._session.auth = local_secret.get('API_KEY')

    def auth_test(self):
        response = self._session.get(f'{API_BASE_URL}/auth/test/')
        return response.json()
