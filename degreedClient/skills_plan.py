import json

from .models.skill_plan import (
    SkillPlan, SkillPlanAttribute,
    SkillFollower, SkillFollowerAttribute)
from .compatibility import scrub


class SkillPlanClient(object):
    """ Required Learnings API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, query=None):
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

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        skillplan = self.client.get_paged('skill-plans', params=params, data=data)
        results = []
        for page in skillplan:
            results.extend([ self._to_skill_plans(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        skillplan = self.client.get("skill-plans/{0}".format(id))
        a_skillplan = skillplan['data']
        return self._to_skill_plans(a_skillplan)

    def get_skill_followers(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        skill_followers = self.client.get("skills-plans/{0}/followers".format(id))
        a_follower = skill_followers['data']
        return self._to_skill_followers(a_follower)


    def _to_skill_followers(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = SkillFollowerAttribute(**data['attributes'])
        return SkillFollower(**data)

    def _to_skill_plans(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = SkillPlanAttribute(**data['attributes'])
        return SkillPlan(**data)

