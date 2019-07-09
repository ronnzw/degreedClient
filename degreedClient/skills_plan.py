import json

from .models.skill_plan import (
    SkillPlan, SkillPlanAttribute,
    SkillFollower, SkillFollowerAttribute)
from .compatibility import scrub


class SkillPlanClient(object):
    """ Skills Plan API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Get all skill plans for the current organization.

        :param start_date: start date eg 2018-11-30
         A maximum of 7 days part between ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: end date eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Amount of providers per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of skill plans.
        :type  next_id: ``str``

        :return: A list of skill plans
        :rtype: ``list`` of :class:`degreedClient.models.skill_plan.SkillPlan`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        skillplan = self.client.get_paged('skill-plans', params=params, data=data)
        results = []
        for page in skillplan:
            results.extend([ self._to_skill_plans(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a skill plan by ID.

        :param id: The ID of the skill plan to retrieve
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.skill_plan.SkillPlan`
        :rtype: :class:`degreedClient.models.skill_plan.SkillPlan`
        """
        skillplan = self.client.get("skill-plans/{0}".format(id))
        a_skillplan = skillplan['data']
        return self._to_skill_plans(a_skillplan)

    def get_skill_followers(self, id):
        """
        Fetch skill followers ID.

        :param id: The unique id of the skill plan.
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.skill_plan.SkillFollower`
        :rtype: :class:`degreedClient.models.skill_plan.SkillFollower`
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

