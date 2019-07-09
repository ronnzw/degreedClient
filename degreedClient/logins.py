import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.login import Login, LoginAttribute


class LoginClient(object):
    """ Logins API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date, end_date, per_page=None, next_id=None):
        """
        Get all logins for the current organization.

        :param start_date: Get logins from this date on. YYYY-MON-DAY
         A maximum of 7 days between ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: Get logins till this date. YYYY-MON-DAY
        :type  end_date: ``str``               

        :param per_page: Amount of logins to per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of groups.
        :type  next_id: ``str``

        :return: A list of logins
        :rtype: ``list`` of :class:`pathgather.models.login.Login`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        login_results = self.client.get_paged('logins?filter[start_date]={0}&filter[end_date]={1}'.format(start_date, end_date), params=params, data=data)
        results = []
        for page in login_results:
            print(page['data'])
            results.extend([ self._to_login(i) for i in page['data']])
        return results

    def _to_login(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = LoginAttribute(**data['attributes'])
        return Login(**data)