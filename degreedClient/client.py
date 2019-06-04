# -*- coding: utf-8 -*-

"""Main module."""
import json
import requests
import urllib.parse as urlparse

from .exceptions import PathgatherApiException #look at this
from .users import UserClient


class DegreedApiClient(object):
    """Main module."""
    results_per_page = 100

    def __init__(self, client_id, client_secret, scope=None, proxy=None, skip_ssl_validation=False):
        """
        Instantiate a new API client

        :param client_id: client_id, e.g. 'a123b456cd789' (request from degreed)
        :type  client_id: ``str``

        :param client_secret: client_secret (request from degreed)
        :type  client_secret: ``str``

        :param scope: The scope of the access rights eg 'users:read'
        :type  scope: ``str``        

        :param proxy: The proxy to connect through
        :type  proxy: ``str``

        :param skip_ssl_validation: Skip SSL validation
        :type  skip_ssl_validation: ``bool``
        """
        self._client_id = client_id

        self._client_secret = client_secret

        self.base_url = "https://api.degreed.com/api/v2"

        self.token_req_url  = "https://degreed.com/oauth/token"

        self.session = requests.Session()

        self.scope_list = 'users:read'

        if scope == None:
            self.scope = self.scope_list
        else:
            self.scope = scope

        if proxy:
            self.session.proxies = {"https": proxy}
        if skip_ssl_validation:
            self.session.verify = False

        payload = {
            'grant_type': "client_credentials",
            'client_id': '{0}'.format(self._client_id),
            'client_secret':'{0}'.format(self._client_secret),
            'scope': '{0}'.format(self.scope),
        }

        headers = {
            'content-type': "application/x-www-form-urlencoded",
            }

        self.response = self.session.post(self.token_req_url, data=payload, headers=headers)
        self.access_data = self.response.json()

        self.expiry_time = self.access_data['expires_in']
        self.access_token = self.access_data['access_token']
        self._refresh_token = self.access_data['refresh_token']

        if self.expiry_time <= 50:
            payload = {
                'grant_type': "refresh_token",
                'refresh_token': self._refresh_token,
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'scope': 'user:read',
            }

            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }

            self.response = session.post(token_req_url, data=payload, headers=headers)
            self.access_data = self.response.json()
            self.access_token = self.access_data['access_token']  
        else:
            pass

        self.session.headers.update(
            {
                "Authorization": "Bearer {0}".format(self.access_token),
            }
        )

        self._users = UserClient(self)

    def get(self, uri, params=None, data=None):
        try:
            if params:
                if "limit" not in params:
                    params["limit"] = self.results_per_page
            else:
                params = {"limit": self.results_per_page}
            result = self.session.get(
                "{0}/{1}".format(self.base_url, uri), params=params, data=data
            )
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text, uri)

    def get_paged(self, uri, params=None, data=None):
        try:
            page = None
            end = False
            while not end:
                result = self.get(uri, params={"next": page}, data=data)
                links_dict = result["links"]
                if 'next' in links_dict:
                    next_page_link = links_dict["next"]
                    yield result
                    if next_page_link:
                        parsed = urlparse.urlparse(next_page_link)
                        next_id = urlparse.parse_qs(parsed.query)["next"]
                        next_page = str(next_id[0])
                        page = next_page
                    else:
                        end = True
                else:
                    break

        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text, uri)

    def post(self, uri, data=None):
        try:
            result = self.session.post("{0}/{1}".format(self.base_url, uri), json=data)
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)

    def put(self, uri, data=None):
        try:
            result = self.session.put("{0}/{1}".format(self.base_url, uri), json=data)
            result.raise_for_status()
            if result.text:
                return result.json()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)

    def delete(self, uri):
        try:
            result = self.session.delete("{0}/{1}".format(self.base_url, uri))
            result.raise_for_status()
        except requests.HTTPError as e:
            raise PathgatherApiException(e.response.text)

    @property
    def users(self):
        """
        Users

        :rtype: :class:`degreedClient.users.UserClient`
        """
        return self._users
###############################################################
#.       Continue from here
###############################################################
























