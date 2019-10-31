# -------------------------------------------------------------------------
# Author: Hayhitee
# --------------------------------------------------------------------------

import re
import sys
from urllib.parse import urlparse, urlencode, urlunparse

DEFAULT_PROTOCOL = 'https'

_EMULATOR_ENDPOINTS = {
}

_CONNECTION_ENDPOINTS = {

}


def get_valid_base_url(protocol, base_url):
    """ This Method will return a valid base url with the protocol
     :parameter: protocol, base_url
     :return: A valid base url with the protocol as the params protocol
     """
    pattern = '(?:http|ftp|https)://'
    base_url = re.sub(pattern, '{}://'.format(protocol), base_url)
    if not re.match(pattern, base_url):
        return '{}://{}'.format(protocol, base_url)
    return base_url


class ServiceConnection:
    _emulator_endpoints = _EMULATOR_ENDPOINTS
    _service_connection_endpoints = _CONNECTION_ENDPOINTS

    def __init__(self, protocol, base_url, secure_connection=False, emulator_base_url=''):
        """
        :param protocol:
        :param base_url:
        :param secure_connection:
        :param emulator_base_url:

        """
        if secure_connection:
            if protocol != 'https':
                raise ValueError('https protocol expected, {} is given'.format(protocol))
            self.protocol = 'https'
        self.protocol = protocol if protocol else DEFAULT_PROTOCOL
        self._base_url = get_valid_base_url(protocol, base_url)
        self._emulator_base_url = get_valid_base_url(protocol, emulator_base_url)

    @staticmethod
    def build_url(base_url, path, params_args='', query=''):
        # Returns a list in the structure of urlparse.ParseResult
        # params_args can be dictionary
        url_parts = list(urlparse(base_url))
        url_parts[2] = path
        url_parts[4] = urlencode(params_args)
        return urlunparse(url_parts)

    @property
    def base_url(self):
        return self._base_url

    @property
    def emulator_base_url(self):
        return self._emulator_base_url

    @property
    def service_connection_endpoints(self):
        print("Getting value")
        return self._service_connection_endpoints

    @service_connection_endpoints.setter
    def service_connection_endpoints(self, value):
        if not isinstance(value, dict):
            raise ValueError('Invalid Data type, Dict is expected')
        self._service_connection_endpoints = value

    @property
    def emulator_endpoints(self):
        print("Getting value")
        return self._emulator_endpoints

    @emulator_endpoints.setter
    def emulator_endpoints(self, value):
        if not isinstance(value, dict):
            raise ValueError('Invalid Data type, Dict is expected')
        self._emulator_endpoints = value

    def get_service_connection_url(self, name):
        return self.build_url(self._base_url, self._service_connection_endpoints.get(name, ''))
        # return connection string
        pass

    def get_emulator_connection_url(self, name):
        # return connection string
        return self.build_url(self._emulator_base_url, self._emulator_endpoints.get(name, ''))
        pass


service_connection = ServiceConnection
