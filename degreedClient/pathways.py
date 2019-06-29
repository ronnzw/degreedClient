import json

from .models.pathway import Pathway, PathwayAttribute
from .models.pathway import Tag, TagAttribute
from .models.pathway import Collaborator, CollaboratorAttribute
from .models.pathway import GrpPathway, GrpPathwayAttribute
from .models.user import User
from .compatibility import scrub


class PathwayClient(object):
    """ Pathway API. """

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

        pathways = self.client.get_paged('pathways', params=params, data=data)
        results = []
        for page in pathways:
            results.extend([ self._to_pathways(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a pathway by ID.

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.pathway.Pathway`
        :rtype: :class:`degreeedClient.degreedClient.models.pathway.Pathway`
        """
        user = self.client.get("pathways/{0}".format(id))
        user_data = user['data']
        return self._to_pathways(user_data)

    def get_pathway_tags(self, id):
        """
        Fetch all tags by ID.

        :param id: The tag id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.pathway.Tag`
        :rtype: :class:`degreeedClient.degreedClient.models.pathway.Tag`
        """
        user = self.client.get("pathways/{0}/tags".format(id))
        user_data = user['data']
        return self._to_tags(user_data)

    def get_pathway_collaborators(self, id):
        """
        Fetch all pathway collaborators by ID.

        :param id: The tag id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.pathway.Tag`
        :rtype: :class:`degreeedClient.degreedClient.models.pathway.Tag`
        """
        user = self.client.get("pathways/{0}/collaborators".format(id))
        user_data = user['data']
        return self._to_collaborators(user_data)

    def get_pathway_groups(self, id):
        """
        Fetch all pathway groups by ID.

        :param id: The tag id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.pathway.GrpPathway`
        :rtype: :class:`degreeedClient.degreedClient.models.pathway.GrpPathway`
        """
        user = self.client.get("pathways/{0}/groups".format(id))
        user_data = user['data']
        return self._to_pathway_groups(user_data)

    def get_pathway_followers(self, id):
        """
        Fetch all pathway groups by ID.

        :param id: The tag id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.pathway.GrpPathway`
        :rtype: :class:`degreeedClient.degreedClient.models.pathway.GrpPathway`
        """
        user = self.client.get("pathways/{0}/followers".format(id))
        user_data = user['data']
        return self._to_pathway_followers(user_data)

    def _to_pathway_followers(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = FollowerAttribute(**data['attributes'])
        return Follower(**data)

    def _to_pathway_groups(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = GrpPathwayAttribute(**data['attributes'])
        return GrpPathway(**data)         

    def _to_collaborators(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = CollaboratorAttribute(**data['attributes'])
        return Collaborator(**data)    

    def _to_tags(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
            data['attributes'] = { x.replace('-','_'): y
            for x,y in data['attributes'].items()}
            data['attributes'] = TagAttribute(**data['attributes'])
        return Tag(**data)        


    def _to_pathways(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = PathwayAttribute(**data['attributes'])
        return Pathway(**data)