import json

from .models.content import Content, ContentAttribute
from .compatibility import scrub


class ContentClient(object):
    """ Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, start_date=None, end_date=None, per_page=None, next_id=None):
        """
        Gets all content.

        :param per_page: Amount of content to per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of content.
        :type  next_id: ``str``

        :param start_date: Content created from this date on
        :type  start_date: ``str``

        :param end_date:  Content created till this date
        :type  end_date: ``str``       

        :return: A list of content
        :rtype: ``list`` of :class:`degreedClient.models.content.Content`
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

        content = self.client.get_paged('content', params=params, data=data)
        results = []
        for page in content:
            results.extend([ self._to_content(i) for i in page['data']])
        return results


    def _to_content(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = ContentAttribute(**data['attributes'])
        return Content(**data)


