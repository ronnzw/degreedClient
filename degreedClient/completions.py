import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.completion import Completion
from .models.completion import CompletionAttribute, NewCompletionAttribute


class CompletionClient(object):
    """ Completion API object """

    def __init__(self, client):
        self.client = client

    def all(self, start_date, end_date, per_page=None, next_id=None):
        """
        Gets all completions from start to end date.

        :param start_date: Get completions from this date on. (YYYY-MON-DAY)
        :type  start_date: ``str``  

        :param end_date: Get completions till this date. (YYYY-MON-DAY)
        :type  end_date: ``str``               

        :param per_page: The amount of completions per page. Max. of 1000.
        :type  per_page: ``str``

        :param next_id: Supplied to retrieve the next batch of content.
        :type  next_id: ``str``



        :return: A list of completions
        :rtype: ``list`` of :class:`degreedClient.models.completion.Completion`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'next': next_id})

        completions = self.client.get_paged(
        	'completions?filter[start_date]={0}&filter[end_date]={1}'.format(start_date, end_date),
        	params=params, data=data)
        results = []
        for page in completions:
            results.extend([ self._to_completions(i) for i in page['data']])
        return results

    def create(self,
        user_id,
        user_identifier_type,
        content_id,
        content_id_type,
        content_type,
        completed_at):
        """
        Create a new completion.

        :param user_id: Unique ID of the user who completed it
         required
        :type  user_id: ``str``

        :param user_identifier_type: Can be either UserId, Email,EmployeeId, 
         AliasUid or AliasEmail. is required
        :type  user_identifier_type: ``str``

        :param content_id: Unique id identifying the content
        :type  content_id: ``str``

        :param content_id_type: Can be either ExternalId, Id or ContentUrl
        :type  content_id_type: ``str``

        :param content_type: Can be either Article, Book, Course, Event or Video
         is required
        :type  content_type: ``str``

        :param completed_at: Date when the completion was created
         is required
        :type  completed_at: ``str``       

        :return: An instance :class:`degreedClient.degreedClient.models.completion.Completion`
        :rtype: :class:`degreeedClient.degreedClient.models.completion.Completion`
        """

        params = {
            "user-id": user_id,
            "user-identifier-type": user_identifier_type,
            "content-id": content_id,
            "content-id-type": content_id_type,
            "content-type": content_type,
            "completed-at": completed_at
            }

        new_completion = self.client.post("completions", {"data":{"attributes": params}})
        a_completion = new_completion['data']
        return self._to_completions(a_completion)

    def update(self,
        id,
        user_id=None,
        user_identifier_type=None,
        content_id=None,
        content_id_type=None,
        content_type=None,
        completed_at=None):
        """
        Create a new completion.

        :param user_id: Unique ID of the user who completed it
         required
        :type  user_id: ``str``

        :param user_identifier_type: Can be either UserId, Email,EmployeeId, 
         AliasUid or AliasEmail. is required
        :type  user_identifier_type: ``str``

        :param content_id: Unique id identifying the content
        :type  content_id: ``str``

        :param content_id_type: Can be either ExternalId, Id or ContentUrl
        :type  content_id_type: ``str``

        :param content_type: Can be either Article, Book, Course, Event or Video
         is required
        :type  content_type: ``str``

        :param completed_at: Date when the completion was created
         is required
        :type  completed_at: ``str``       

        :return: An instance :class:`degreedClient.degreedClient.models.completion.Completion`
        :rtype: :class:`degreeedClient.degreedClient.models.completion.Completion`
        """

        params = {}
        if user_id:
            params["user-id"] = user_id
        if user_identifier_type:
            params["user-identifier-type"] = user_identifier_type
        if content_id:
            params["content-id"] = content_id
        if content_id_type:
            params["content-id-type"] = content_id_type
        if content_type:
            params["content-type"] = content_type
        if completed_at:
            params["completed-at"] = completed_at


        new_completion = self.client.patch("completions/{0}".format(id), {"data":{"attributes": params}})
        a_completion = new_completion['data']
        return self._to_completions(a_completion)

    def delete(self, id):
        """
        Delete an book by ID.

        :param id: Completion ID to be delectes
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("completions/{0}".format(id))

    def _to_completions(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = CompletionAttribute(**data['attributes'])
        	data['attributes'] = NewCompletionAttribute(**data['attributes'])
        return Completion(**data)