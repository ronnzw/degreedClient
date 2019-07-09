import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.group import Group, GroupAttribute
from .models.attribute import Attribute


class GroupClient(object):
    """ Groups API object """
    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Get all groups for the current organization

        :param per_page: Amount of groups to per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of groups.
        :param next_id: ``str``

        :return: A list of groups
        :rtype: ``list`` of :class:`degreedClient.models.group.Group`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        groups = self.client.get_paged('groups', params=params, data=data)
        results = []
        for page in groups:
            results.extend([ self._to_groups(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a specific group for the current organization

        :param id: id used to get a specific group
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.group.Group`
        :rtype: :class:`degreedClient.models.group.Group`
        """
        user = self.client.get("groups/{0}".format(id))
        user_data = user['data']
        return self._to_groups(user_data)

    def group_users_list(self, id):
        """
        Fetch a list of users which are a member of this group.

        :param id: id used to get a specific group
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.group.Group`
        :rtype: :class:`degreedClient.models.group.Group`
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
