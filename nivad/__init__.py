import json
import logging

import certifi
import jwt
import urllib3

from nivad.push import NivadNotificationAPI

DEBUG = True
logger = logging.getLogger("nivad")


def _get_connection_url():
    return '/api/v1/' if DEBUG else '/v1/'


def _get_connection_pool():
    if DEBUG:
        return urllib3.HTTPConnectionPool('127.0.0.1:8000')
    else:
        return urllib3.HTTPSConnectionPool(
            'api.nivad.io',
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )


class NivadAPI:
    base_url = _get_connection_url()
    connection_pool = _get_connection_pool()

    def __init__(self, application_id, **kwargs):
        self.application_id = application_id
        self.secrets = {
            'push': kwargs.get('push_secret', None),
            'push_api': kwargs.get('push_api_secret', None),
            'billing': kwargs.get('billing_secret', None),
            'master': kwargs.get('master_secret', None),
        }

    def get_notification_api(self):
        return NivadNotificationAPI(self)

    def post(self, url, data, token_type='master', extra_headers=None):
        return self.__request('post', url, data, token_type, extra_headers)

    def get(self, url, data, token_type='master', extra_headers=None):
        return self.__request('get', url, data, token_type, extra_headers)

    def put(self, url, data, token_type='master', extra_headers=None):
        return self.__request('put', url, data, token_type, extra_headers)

    def delete(self, url, data, token_type='master', extra_headers=None):
        return self.__request('delete', url, data, token_type, extra_headers)

    def __request(self, method, url, data, token_type='master', extra_headers=None):
        if not extra_headers:
            extra_headers = dict()

        assert type(extra_headers) == dict
        assert token_type in self.secrets

        method = method.upper()

        secret = (token_type, self.secrets[token_type])
        if not secret[1]:
            secret = ('master', self.secrets['master'])

        assert secret[1], 'Please provide appropriate secrets'

        authorization_token = jwt.encode({
            'typ': secret[0],
            'aid': self.application_id
        }, secret[1]).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'bearer %s' % str(authorization_token)
        }

        if 'Authorization' in extra_headers:
            del extra_headers['Authorization']

        headers.update(extra_headers)

        if '{' in url:
            url = url.format(**data)
            # TODO: remove formatted data from dictionary

        request_url = '%s%s' % (_get_connection_url(), url)

        logger.info("Making %s request to %s -- Headers: %s" % (method, request_url, headers))
        if method == 'GET':
            response = NivadAPI.connection_pool.request(method, request_url, headers=headers, fields=data)
        else:
            if not type(data) == str:
                data = json.dumps(data)
            data = data.encode('utf-8')
            response = NivadAPI.connection_pool.request(method, request_url, headers=headers, body=data)

        return response

__all__ = [NivadAPI]