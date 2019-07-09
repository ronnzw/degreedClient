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

    def all(self, start_date=None, end_date=None, per_page=None, next_id=None):
        """
        Gets all pathways for the current organization.

        :param start_date: Get pathways modified from this date on.
         A maximum of 7 days between ``start_date`` and ``end_date``
        :type  start_date: ``str``

        :param end_date: Get pathways modified till this date.
        :type  end_date: ``str``        

        :param per_page:   Amount of pathways per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of pathways.
        :type  next_id: ``str``

        :return: A list of pathways
        :rtype: ``list`` of :class:`degreedClient.models.pathway.Pathway`
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

        pathways = self.client.get_paged('pathways', params=params, data=data)
        results = []
        for page in pathways:
            results.extend([ self._to_pathways(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch all data on a specific pathway.

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.pathway.Pathway`
        :rtype: :class:`degreedClient.models.pathway.Pathway`
        """
        user = self.client.get("pathways/{0}".format(id))
        user_data = user['data']
        return self._to_pathways(user_data)

    def get_pathway_tags(self, id):
        """
        Fetch all tags for the selected pathway

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.pathway.Tag`
        :rtype: :class:`degreedClient.models.pathway.Tag`
        """
        user = self.client.get("pathways/{0}/tags".format(id))
        user_data = user['data']
        return self._to_tags(user_data)

    def get_pathway_collaborators(self, id):
        """
        Fetch all collaborators for the selected pathway

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.pathway.Collaborator`
        :rtype: :class:`degreedClient.models.pathway.Collaborator`
        """
        user = self.client.get("pathways/{0}/collaborators".format(id))
        user_data = user['data']
        return self._to_collaborators(user_data)

    def get_pathway_groups(self, id):
        """
        Fetch all groups for the selected pathway

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.pathway.GrpPathway`
        :rtype: :class:`degreedClient.models.pathway.GrpPathway`
        """
        user = self.client.get("pathways/{0}/groups".format(id))
        user_data = user['data']
        return self._to_pathway_groups(user_data)

    def get_pathway_followers(self, id):
        """
        Fetch all followers for the selected pathway.

        :param id: The pathway id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.pathway.Follower`
        :rtype: :class:`degreedClient.models.pathway.Follower`
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