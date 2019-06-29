import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.group import Group, GroupAttribute
from .models.attribute import Attribute


class GroupClient(object):
    """ Users API object """
    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, query=None):
        """
        Get all users (will page results out)

        :param per_page: Starting page
        :type  per_page: ``int``

        :param query: Extra query parameters
        :param query: ``dict``

        :return: A list of users
        :rtype: ``list`` of :class:`degreedClient.degreedClient.models.user.User`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        groups = self.client.get_paged('groups', params=params, data=data)
        results = []
        for page in groups:
            results.extend([ self._to_groups(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        user = self.client.get("groups/{0}".format(id))
        user_data = user['data']
        return self._to_groups(user_data)

    def group_users_list(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        user = self.client.get("groups/{0}/users".format(id))
        user_data = user['data']
        return self._to_groups(user_data)        

    def _to_groups(self, data):
        scrub(data)

        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data["attributes"] = GroupAttribute(**data["attributes"])
        return Group(**data)
