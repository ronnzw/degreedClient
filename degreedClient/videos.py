import json

from .models.content import Video, VideoAttribute
from .compatibility import scrub


class VideoClient(object):
    """ Video Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Gets all Videos.

        :param per_page: Amount of content to per page. Max of 1.000
        :type  per_page: ``int``

        :param next_id: Supplied to retrieve the next batch of content.
        :type  next_id: ``str``      

        :return: A list of Videos
        :rtype: ``list`` of :class:`degreedClient.models.content.Video`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        videos = self.client.get_paged('content/videos', params=params, data=data)
        results = []
        for page in videos:
            results.extend([ self._to_videos(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a video by ID.

        :param id: The video id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.content.Video`
        :rtype: :class:`degreedClient.models.content.Video`
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
        Create a Video Content.

        :param external_id: The course's external id, is required
        :type  external_id: ``str``        

        :param title: The course title, is required
        :type  title: ``str``

        :param duration: Length of the course. Type is supplied with ``duration-type``
        :type  duration: ``int``

        :param duration_type: Seconds, Minutes, Hours or Days
        :type  duration_type: ``str``

        :param summary: Summary of the video
        :type  summary: ``str`` 

        :param url: URL location where more information can be found
        :type  url: ``str``

        :param obsolete: If the course should be marked as obsolete
        :type  obsolete: ``bool``

        :param image_url: Cover image of the video
        :type  image_url: ``str``

        :param language: Spoken language of the video
        :type  language: ``str``

        :param publish_date: The date the video is published
        :type  publish_date: ``str``                                                                                  

        :return: An instance :class:`degreedClient.models.content.Video`
        :rtype: :class:`degreedClient.models.content.Video`
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
        Update a Video Content.

        :param id: The ID of the video to update
        :type  id: ``str``          

        :param external_id: The course's external id, is required
        :type  external_id: ``str``        

        :param title: The course title, is required
        :type  title: ``str``

        :param duration: Length of the course. Type is supplied with ``duration-type``
        :type  duration: ``int``

        :param duration_type: Seconds, Minutes, Hours or Days
        :type  duration_type: ``str``

        :param summary: Summary of the video
        :type  summary: ``str`` 

        :param url: URL location where more information can be found
        :type  url: ``str``

        :param obsolete: If the course should be marked as obsolete
        :type  obsolete: ``bool``

        :param image_url: Cover image of the video
        :type  image_url: ``str``

        :param language: Spoken language of the video
        :type  language: ``str``

        :param publish_date: The date the video is published
        :type  publish_date: ``str``                                                                                  

        :return: An instance :class:`degreedClient.models.content.Video`
        :rtype: :class:`degreedClient.models.content.Video`
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
        Delete a video by ID.

        :param id: The video ID
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