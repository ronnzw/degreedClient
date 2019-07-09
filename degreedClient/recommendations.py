import json

from .models.recommendation import Recommendation, RecoAttribute
from .compatibility import scrub


class RecommendationClient(object):
    """ Recommendation API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date, end_date, per_page=None, next_id=None):
        """
        Get all recommendations.

        :param start_date: Get recommendations from this date on. eg 2018-11-30
         A a maximum of 7 days between ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: Get recommendations till this date. eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Amount of recommendations per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of recommendations.
        :type  next_id: ``str``

        :return: A list of recommendations
        :rtype: ``list`` of :class:`degreedClient.models.recommendation.Recommendation`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        recommendations = self.client.get_paged(
        	'recommendations?filter[start_date]={0}&filter[end_date]={1}'.format(start_date, end_date),
        	params=params, data=data)
        results = []
        for page in recommendations:
            results.extend([ self._to_recommendation(i) for i in page['data']])
        return results

    def _to_recommendation(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = RecoAttribute(**data['attributes'])
        return Recommendation(**data)