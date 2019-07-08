import json

from .models.search_term import SearchTerm, SearchTermAttribute
from .compatibility import scrub


class SearchTermClient(object):
    """ Certifiable skills API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Get all certifiable skills.

        :param per_page: Amount of certifiable skills per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of user skills.
        :type  next_id: ``str``

        :return: A list of required learnings
        :rtype: ``list`` of :class:`degreedClient.models.certifiable_skill.CertifiableSkill`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        search_term = self.client.get_paged('search-terms', params=params, data=data)
        results = []
        for page in search_term:
            results.extend([ self._to_search_term(i) for i in page['data']])
        return results

    def _to_search_term(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = SearchTermAttribute(**data['attributes'])
        return SearchTerm(**data)