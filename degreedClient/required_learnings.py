import json

from .models.required_learning import ReqLearning, LearningsAttribute
from .compatibility import scrub


class RequiredLearningsClient(object):
    """ Required Learnings API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date, end_date, per_page=None, next_id=None):
        """
        Gets all learning requirements.

        :param start_date: Get required learnings from this date on. eg 2018-11-30
        :type  start_date: ``str``

        :param end_date: Get required learnings till this date. eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Amount of required learnings per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of required learning.
        :type  next_id: ``str``

        :return: A list of required learnings
        :rtype: ``list`` of :class:`degreedClient.models.required_learning.ReqLearning`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'next': next_id})

        learnings_req = self.client.get_paged(
        	'required-learning?filter[start_date]={0}&filter[end_date]={1}'.format(start_date, end_date),
        	params=params, data=data)
        results = []
        for page in learnings_req:
            results.extend([ self._to_required_learnings(i) for i in page['data']])
        return results

    def _to_required_learnings(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = LearningsAttribute(**data['attributes'])
        return ReqLearning(**data)