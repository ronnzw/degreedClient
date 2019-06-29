import json

from .models.content import Content, ContentAttribute
from .models.user import User
from .compatibility import scrub


class ContentClient(object):
    """ Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, start_filter=None, end_filter=None, query=None):
        """
        Get all content.

        :param from_page: Get from page
        :type  from_page: ``str``

        :param query: Additional filter query
            (see https://docs.pathgather.com/docs/filtering)
        :type  query: ``dict``

        :param filter: Additional type filter, e.g. "shared", "official", "pathgather"
        :type  filter: ``str``

        :return: A list of content
        :rtype: ``list`` of :class:`pathgather.models.content.Content`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page
        if start_filter is not None:
        	params['filter[start_date]'] = start_filter
        if end_filter is not None:
        	params['filter[end_date]'] = end_filter

        data = None
        if query is not None:
            data = json.dumps({'q': query})

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


