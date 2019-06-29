import json

from .models.user_follower import UserFollower, UserFollowersAttribute
from .compatibility import scrub


class UserFollowersClient(object):
    """ Required Learnings API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date=None, end_date=None, per_page=None, query=None):
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
        if start_date is not None:
            params['filter[start_date]'] = start_filter
        if end_date is not None:
            params['filter[end_date]'] = end_filter

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        user_followers = self.client.get_paged('user-followers', params=params, data=data)
        results = []
        for page in user_followers:
            results.extend([ self._to_user_follower(i) for i in page['data']])
        return results

    def _to_user_follower(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = UserFollowerAttribute(**data['attributes'])
        return UserFollower(**data)