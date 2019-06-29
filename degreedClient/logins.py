import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.login import Login, LoginAttribute


class LoginClient(object):
    """ Completion API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date, end_date, per_page=None, query=None):
        """
        Get all content.

        :param from_page: Get from page
        :type  from_page: ``str``

        :param query: Additional filter query
            (see https://docs.pathgather.com/docs/filtering)
        :type  query: ``dict``

        :param filter: Additional type filter, e.g. "shared", "official", "pathgather"
        :type  filter: ``str``

        :return: A list of content
        :rtype: ``list`` of :class:`pathgather.models.content.Content`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        completions = self.client.get_paged(
        	'logins?filter[start_date]={0}&filter[end_date]={1}'.format(start_date, end_date),
        	params=params, data=data)
        results = []
        for page in completions:
            results.extend([ self._to_login(i) for i in page['data']])
        return results

    def _to_login(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = LoginAttribute(**data['attributes'])
        return Login(**data)