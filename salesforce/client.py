import requests
from salesforce.decorators import access_token_required
from salesforce.exceptions import UnknownError, BadOAuthTokenError, BadRequestError, TokenError
from urllib.parse import unquote, urlencode


class Client(object):
    BASE_URL = '{}/services/data/'
    SALESFORCE_REQUEST_TOKEN_URL = 'https://login.salesforce.com/services/oauth2/token'
    SALESFORCE_AUTHORIZE_URL = 'https://login.salesforce.com/services/oauth2/authorize'

    def __init__(self, client_id, client_secret, version, instance_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.instance_url = self.BASE_URL.format(instance_url)
        self.rest_url = self.instance_url + '{}/'.format(version)
        if version.startswith('v'):
            version = version[1:]
        self.version = version
        self.access_token = None
        self._refresh_token = None
        self.resource_urls = {}

    def _get_resource_url(self, name):
        url = self.resource_urls.get(name, None)
        if url:
            return url
        user_info = self.get_user_info()
        for k, v in user_info['urls'].items():
            self.resource_urls[k] = v.replace('{version}', self.version)
        return self.resource_urls.get(name, None)

    def set_access_token(self, token):
        if isinstance(token, dict):
            self.access_token = token['access_token']
            if 'refresh_token' in token:
                self._refresh_token = token['refresh_token']
        else:
            self.access_token = token

    def authorization_url(self, redirect_uri):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri
        }
        url = self.SALESFORCE_AUTHORIZE_URL
        return '{}?{}'.format(url, urlencode(params))

    def exchange_code(self, redirect_uri, code):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': unquote(code),
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        return self._request('POST', self.SALESFORCE_REQUEST_TOKEN_URL, data=data, headers=headers)

    def refresh_token(self):
        if not self._refresh_token:
            return None
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': unquote(self._refresh_token),
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        return self._request('POST', self.SALESFORCE_REQUEST_TOKEN_URL, data=data, headers=headers)

    @access_token_required
    def get_user_info(self):
        return self._request('GET', 'https://login.salesforce.com/services/oauth2/userinfo')

    def get_versions(self):
        return self._get(self.instance_url)

    @access_token_required
    def get_resources_by_version(self):
        return self._get(self.rest_url)

    @access_token_required
    def get_limits(self):
        return self._get(self.rest_url + 'limits/')

    @access_token_required
    def get_describe_global(self):
        return self._get(self.rest_url + 'sobjects/')

    @access_token_required
    def get_sobject(self, sobject):
        return self._get(self.rest_url + 'sobjects/{}/'.format(sobject))

    @access_token_required
    def create_sobject(self, sobject, data):
        return self._post(self.rest_url + 'sobjects/{}/'.format(sobject), json=data)

    @access_token_required
    def get_sobject_describe(self, sobject):
        return self._get(self.rest_url + 'sobjects/{}/describe/'.format(sobject))

    def create_apex_class(self, name, body):
        data = {
            'ApiVersion': self.version,
            'Body': body,
            'Name': name
        }
        url = self.rest_url + 'tooling/sobjects/ApexClass'
        return self._request('POST', url, json=data)

    def delete_apex_class(self, apex_class_id):
        url = self.rest_url + 'tooling/sobjects/ApexClass/{}'.format(apex_class_id)
        return self._request('DELETE', url)

    def create_remote_site(self, name, url):
        data = '<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><env:Header><urn:SessionHeader xmlns:urn="http://soap.sforce.com/2006/04/metadata"><urn:sessionId>{sessionId}</urn:sessionId></urn:SessionHeader></env:Header><env:Body><createMetadata xmlns="http://soap.sforce.com/2006/04/metadata"><metadata xsi:type="RemoteSiteSetting"><fullName>{name}</fullName><isActive>true</isActive><url>{url}</url></metadata></createMetadata></env:Body></env:Envelope>'
        data = data.replace('{name}', name).replace('{url}', url).replace('{sessionId}', self.access_token)

        headers = {
            'SOAPAction': 'RemoteSiteSetting',
            'Content-Type': 'text/xml'
        }
        url = self._get_resource_url('metadata')
        return self._request('POST', url, data=data, headers=headers)

    def create_apex_trigger(self, name, body, sobject):
        data = {
            'ApiVersion': self.version,
            'Body': body,
            'Name': name,
            'TableEnumOrId': sobject
        }
        url = self.rest_url + 'tooling/sobjects/ApexTrigger'
        return self._request('POST', url, json=data)

    def delete_apex_trigger(self, apex_trigger_id):
        url = self.rest_url + 'tooling/sobjects/ApexTrigger/{}'.format(apex_trigger_id)
        return self._request('DELETE', url)

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if headers:
            _headers.update(headers)
        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise BadRequestError(r)
        if status_code == 401:
            raise TokenError(r)
        if status_code == 403:
            raise BadOAuthTokenError(r)
        raise UnknownError(r)
