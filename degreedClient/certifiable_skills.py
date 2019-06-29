import json

from .models.certifiable_skill import CertifiableSkill, CertifiableSkillAttribute
from .compatibility import scrub


class CertifiableSkillClient(object):
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

        user_skills = self.client.get_paged('certifiable-skills', params=params, data=data)
        results = []
        for page in user_skills:
            results.extend([ self._to_provider(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        user_skill = self.client.get("certifiable-skills/{0}".format(id))
        a_user_skill = user_skill['data']
        return self._to_certifiable_skill(a_user_skill)

    def _to_certifiable_skill(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = CertifiableSkillAttribute(**data['attributes'])
        return CertifiableSkill(**data)