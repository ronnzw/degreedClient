import json

from .models.user_skill import UserSkill, UserSkillAttribute
from .compatibility import scrub


class UserSkillClient(object):
    """ User Skill API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date=None, end_date=None, per_page=None, next_id=None):
        """
        Gets all users skills for the current organisation.

        :param start_date: start date eg 2018-11-30
         A maximum of 7 days between ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: end date eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Get from page
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of user skills.
        :type  next_id: ``str``

        :return: A list of user skills
        :rtype: ``list`` of :class:`degreedClient.models.user_skill.UserSkill`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page
        if start_date is not None:
            params['filter[start_date]'] = start_date
        if end_date is not None:
            params['filter[end_date]'] = end_date

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        user_skill = self.client.get_paged('user-skills', params=params, data=data)
        results = []
        for page in user_skill:
            results.extend([ self._to_user_skill(i) for i in page['data']])
        return results

    def _to_user_skill(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = UserSkillAttribute(**data['attributes'])
        return UserSkill(**data)