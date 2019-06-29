import json

from .models.provider import (
    Provider, ProviderAttribute,
    SpecificProvider, SpecificProviderAttribute,
    ProviderLicence, ProviderLicenceAttribute)
from .compatibility import scrub


class ProviderClient(object):
    """ Required Learnings API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, query=None):
        """
        Get all learning requirements.

        :param start_date: start date eg 2018-11-30
        :type  start_date: ``str``

        :param end_date: end date eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Get from page
        :type  per_page: ``str``

        :param query: Additional filter query
            (see https://api.degreed.com/docs/#get-all-required-learnings)
        :type  query: ``dict``

        :return: A list of required learnings
        :rtype: ``list`` of :class:`degreedClient.models.required_learning.ReqLearning`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        providers = self.client.get_paged('providers', params=params, data=data)
        results = []
        for page in providers:
            results.extend([ self._to_provider(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        specific_provider = self.client.get("providers/{0}".format(id))
        a_specific_provider = specific_provider['data']
        return self._to_specific_provider(a_specific_provider)

    def get_provider_licence(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        provider_licence = self.client.get("providers/{0}/licences".format(id))
        a_provider_licence = provider_licence['data']
        return self._to_specific_provider(a_provider_licence)


    def _to_provider_licence(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = ProviderLicenceAttribute(**data['attributes'])
        return ProviderLicence(**data)

    def _to_provider(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = ProviderAttribute(**data['attributes'])
        return Provider(**data)

    def _to_specific_provider(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = SpecificProviderAttribute(**data['attributes'])
        return SpecificProvider(**data)