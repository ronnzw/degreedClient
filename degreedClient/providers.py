import json

from .models.provider import (
    Provider, ProviderAttribute,
    SpecificProvider, SpecificProviderAttribute,
    ProviderLicence, ProviderLicenceAttribute)
from .compatibility import scrub


class ProviderClient(object):
    """ Providers API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Get all providers for the current organization.

        :param per_page: Amount of providers per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id:   Supplied to retrieve the next batch of groups.
        :type  next_id: ``str``

        :return: A list of providers
        :rtype: ``list`` of :class:`degreedClient.models.provider.Provider`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        providers = self.client.get_paged('providers', params=params, data=data)
        results = []
        for page in providers:
            results.extend([ self._to_provider(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a specific provider.

        :param id:  The ID of the provider to retrieve
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.provider.SpecificProvider`
        :rtype: :class:`degreedClient.models.provider.SpecificProvider`
        """
        specific_provider = self.client.get("providers/{0}".format(id))
        a_specific_provider = specific_provider['data']
        return self._to_specific_provider(a_specific_provider)

    def get_provider_licence(self, id):
        """
        Fetch provider licences for a specific provider

        :param id: The unique id of the provider.
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.provider.ProviderLicence`
        :rtype: :class:`degreedClient.models.provider.ProviderLicence`
        """
        provider_licence = self.client.get("providers/{0}/licences".format(id))
        a_provider_licence = provider_licence['data']
        return self._to_provider_licence(a_provider_licence)


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