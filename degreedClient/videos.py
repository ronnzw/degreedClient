import json

from .models.content import ( Content, ContentAttribute, ArticleAttribute,
    Article, BookAttribute, Book, Video, VideoAttribute)
from .models.user import User
from .compatibility import scrub


class VideoClient(object):
    """ Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, query=None):
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

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        videos = self.client.get_paged('content/videos', params=params, data=data)
        results = []
        for page in videos:
            results.extend([ self._to_videos(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        video = self.client.get("content/videos/{0}".format(id))
        a_video = video['data']
        return self._to_videos(a_video)

    def create(self,
        external_id,
        title,
        duration,
        duration_type,
        summary=None,        
        url=None,
        obsolete=None,        
        image_url=None,       
        language=None,
        publish_date=None):
        """
        Create an article.

        :param name: The article's external id, is required
        :type  name: ``str``

        :param job_title: The article's title, is required
        :type  job_title: ``str``

        :param job_title: The article's url, is required
        :type  job_title: ``str``

        :param job_title: The article's number of words, is required
        :type  job_title: ``int``

        :param job_title: The article's summary, no required
         is optional
        :type  job_title: ``str``

        :param job_title: The article's image url 
         is optional
        :type  job_title: ``str``       

        :return: An instance :class:`degreedClient.degreedClient.models.content.Article`
        :rtype: :class:`degreeedClient.degreedClient.models.content.Article`
        """

        params = {
            "external-id": external_id,
            "title": title,
            "duration": duration,
            "duration-type": duration_type
            }
        
        if url:
            params['url'] = url
        if image_url:
            params['image-url'] = image_url
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if publish_date:
            params['publish-date'] = publish_date
        if language:
            params['language'] = language

        video = self.client.post("content/videos", {"data":{"attributes": params}})
        a_video = video['data']
        return self._to_videos(a_video)

    def update(self,
        id,
        external_id=None,
        title=None,
        duration=0,
        duration_type=None,
        summary=None,        
        url=None,
        obsolete=None,        
        image_url=None,       
        language=None,
        publish_date=None):
        """
        Create an article.

        :param name: The article's external id, is required
        :type  name: ``str``

        :param job_title: The article's title, is required
        :type  job_title: ``str``

        :param job_title: The article's url, is required
        :type  job_title: ``str``

        :param job_title: The article's number of words, is required
        :type  job_title: ``int``

        :param job_title: The article's summary, no required
         is optional
        :type  job_title: ``str``

        :param job_title: The article's image url 
         is optional
        :type  job_title: ``str``       

        :return: An instance :class:`degreedClient.degreedClient.models.content.Article`
        :rtype: :class:`degreeedClient.degreedClient.models.content.Article`
        """

        params = {}


        if external_id:
            params['external-id'] = external_id
        if title:
            params['title'] = title
        if duration:
            params["duration"] = duration
        if duration_type:
            params['duration-type'] = duration_type
        if url:
            params['url'] = url
        if image_url:
            params['image-url'] = image_url
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if publish_date:
            params['publish-date'] = publish_date
        if language:
            params['language'] = language

        video = self.client.patch("content/videos/{0}".format(id), {"data":{"attributes": params}})
        a_video = video['data']
        return self._to_videos(a_video)

    def delete(self, id):
        """
        Delete an book by ID.

        :param id: The book ID
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("content/videos/{0}".format(id))

    def _to_videos(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = VideoAttribute(**data['attributes'])
        return Video(**data)