import json

from .models.certifiable_skill import CertifiableSkill, CertifiableSkillAttribute
from .compatibility import scrub


class CertifiableSkillClient(object):
    """ Certifiable skills API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Get all certifiable skills.

        :param per_page: Amount of certifiable skills per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of user skills.
        :type  next_id: ``str``

        :return: A list of required learnings
        :rtype: ``list`` of :class:`degreedClient.models.certifiable_skill.CertifiableSkill`
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
        Fetch a specific certifiable skill

        :param id: id used to get a specific certifiable skill
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.certifiable_skill.CertifiableSkill`
        :rtype: :class:`degreedClient.models.certifiable_skill.CertifiableSkill`
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