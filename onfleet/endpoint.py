from onfleet.request import Request


class Endpoint:
    '''
    Onfleet API endpoint.
    '''

    def __init__(self, name, basic_methods, session):
        self.name = name
        self.session = session
        self._add_basic_methods(basic_methods)

    def _add_basic_methods(self, basic_methods):
        if not basic_methods:
            return

        uri = f'/{self.name}'  # e.g. '/admins'

        if 'GET' in basic_methods:
            self.get = Request('GET', uri, self.session)
        if 'POST' in basic_methods:
            self.create = Request('POST', uri, self.session)

        uri = f'{uri}/:{self.name[:-1]}Id'  # e.g. '/admins' --> '/admins/:adminId'

        if 'PUT' in basic_methods:
            self.update = Request('PUT', uri, self.session)
        if 'DELETE' in basic_methods:
            self.deleteOne = Request('DELETE', uri, self.session)
