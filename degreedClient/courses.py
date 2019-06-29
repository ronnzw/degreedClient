import json

from .models.content import Course, CourseAttribute
from .models.user import User
from .compatibility import scrub


class CourseClient(object):
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

        courses = self.client.get_paged('content/courses', params=params, data=data)
        results = []
        for page in courses:
            results.extend([ self._to_courses(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        course = self.client.get("content/courses/{0}".format(id))
        a_course = course['data']
        return self._to_courses(a_course)

    def create(self,
        title,        
        external_id,
        duration,
        duration_type,
        provider_code=None,
        cost_units=0,
        cost_unit_type=None,
        _format=None,
        difficulty=None,
        video_url=None,        
        summary=None,        
        url=None,
        obsolete=False,        
        image_url=None,       
        language=None):
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
            "title": title,        
            "external-id": external_id,
            "duration": duration,
            "duration-type": duration_type
            }
        if provider_code:
            params['provider-code'] = provider_code
        if cost_units:
            params['cost-units'] = cost_units
        if cost_unit_type:
            params['cost-unit-type'] = cost_unit_type
        if _format:
            params['format'] = _format
        if difficulty:
            params['difficulty'] = difficulty
        if video_url:
            params['video-url'] = video_url
        if url:
            params['url'] = url
        if image_url:
            params['image-url'] = image_url
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if language:
            params['language'] = language

        course = self.client.post("content/courses", {"data":{"attributes": params}})
        a_course = course['data']
        return self._to_courses(a_course)

    def update(self,
        id,
        title=None,        
        external_id=None,
        duration=0,
        duration_type=None,
        provider_code=None,
        cost_units=0,
        cost_unit_type=None,
        _format=None,
        difficulty=None,
        video_url=None,        
        summary=None,        
        url=None,
        obsolete=False,        
        image_url=None,       
        language=None):
        """
        Create a course.

        :param name: The course's external id, is required
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

        if title:
            params["title"] = title
        if external_id:       
            params["external-id"] = external_id
        if duration:
            params["duration"] = duration
        if duration_type:
            params["duration-type"] = duration_type
        if provider_code:
            params['provider-code'] = provider_code
        if cost_units:
            params['cost-units'] = cost_units
        if cost_unit_type:
            params['cost-unit-type'] = cost_unit_type
        if _format:
            params['format'] = _format
        if difficulty:
            params['difficulty'] = difficulty
        if video_url:
            params['video-url'] = video_url
        if url:
            params['url'] = url
        if image_url:
            params['image-url'] = image_url
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if language:
            params['language'] = language

        course = self.client.patch("content/courses/{0}".format(id), {"data":{"attributes": params}})
        a_course = course['data']
        return self._to_courses(a_course)

    def delete(self, id):
        """
        Delete an book by ID.

        :param id: The book ID
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("content/courses/{0}".format(id))

    def _to_courses(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = CourseAttribute(**data['attributes'])
        return Course(**data)