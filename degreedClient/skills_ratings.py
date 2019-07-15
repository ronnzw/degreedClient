import json

from .models.skills_rating import SkillRating, SkillRatingAttribute
from .compatibility import scrub


class SkillRatingClient(object):
    """ Skill Ratings API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date=None, end_date=None, per_page=None, next_id=None):
        """
        Gets all skills ratings.

        :param start_date: start date eg 2018-11-30
         A maximum of 7 days between the ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: end date eg 2018-11-30
        :type  end_date: ``str``

        :param per_page: Amount of skill ratings per page. Max of 1.000.
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of groups.
        :type  next_id: ``strt``

        :return: A list of skill ratings
        :rtype: ``list`` of :class:`degreedClient.models.skills_rating.SkillRating`
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

        rating_skill = self.client.get_paged('skill-ratings', params=params, data=data)
        results = []
        for page in rating_skill:
            results.extend([ self._to_skill_rating(i) for i in page['data']])
        return results

    def _to_skill_rating(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = SkillRatingAttribute(**data['attributes'])
        return SkillRating(**data)