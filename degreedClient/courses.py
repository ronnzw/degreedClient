import json

from .models.content import Course, CourseAttribute
from .compatibility import scrub


class CourseClient(object):
    """ Course Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Gets all Courses.

        :param per_page:    Amount of content to per page. Max of 1.000
        :type  per_page: ``str``

        :param next_id: Supplied to retrieve the next batch of content.
        :type  next_id: ``str``      

        :return: A list of content
        :rtype: ``list`` of :class:`degreedClient.models.content.Course`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id})

        courses = self.client.get_paged('content/courses', params=params, data=data)
        results = []
        for page in courses:
            results.extend([ self._to_courses(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch course by ID.

        :param id: The course id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.content.Course`
        :rtype: :class:`degreedClient.models.content.Course`
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
        Create a Course.

        :param title: The course title, is required
        :type  title: ``str``

        :param external_id: The course's external id, is required
        :type  external_id: ``str``

        :param duration: Length of the course. Type is supplied with ``duration-type``
        :type  duration: ``int``

        :param duration_type: Seconds, Minutes, Hours or Days
        :type  duration_type: ``str``

        :param provider_code: Unique provider code
        :type  provider_code: ``str``

        :param cost_units: Units for the amount of cost
        :type  cost_units: ``int`` 

        :param cost_unit_type: The cost unit type, can be any valuta
        :type  cost_unit_type: ``str``

        :param _format: Format the course is takes
        :type  _format: ``str``

        :param difficulty: Describing the difficulty of taking the course
        :type  difficulty: ``str``

        :param video_url: If the course has a video, supply it here
        :type  video_url: ``str``

        :param summary: Summary of the course
        :type  summary: ``str`` 

        :param url: URL location where more information can be found
        :type  url: ``str``

        :param obsolete: If the course should be marked as obsolete
        :type  obsolete: ``bool``

        :param image_url: Cover image of the course
        :type  image_url: ``str``

        :param language: Spoken language of the course
        :type  language: ``str``                                                                            

        :return: An instance :class:`degreedClient.models.content.Course`
        :rtype: :class:`degreedClient.models.content.Course`
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
        Update a Course.

        :param id: The ID of the course to update
        :type  id: ``str``        

        :param title: The course title, is required
        :type  title: ``str``

        :param external_id: The course's external id, is required
        :type  external_id: ``str``

        :param duration: Length of the course. Type is supplied with ``duration-type``
        :type  duration: ``int``

        :param duration_type: Seconds, Minutes, Hours or Days
        :type  duration_type: ``str``

        :param provider_code: Unique provider code
        :type  provider_code: ``str``

        :param cost_units: Units for the amount of cost
        :type  cost_units: ``int`` 

        :param cost_unit_type: The cost unit type, can be any valuta
        :type  cost_unit_type: ``str``

        :param _format: Format the course is takes
        :type  _format: ``str``

        :param difficulty: Describing the difficulty of taking the course
        :type  difficulty: ``str``

        :param video_url: If the course has a video, supply it here
        :type  video_url: ``str``

        :param summary: Summary of the course
        :type  summary: ``str`` 

        :param url: URL location where more information can be found
        :type  url: ``str``

        :param obsolete: If the course should be marked as obsolete
        :type  obsolete: ``bool``

        :param image_url: Cover image of the course
        :type  image_url: ``str``

        :param language: Spoken language of the course
        :type  language: ``str``                                                                            

        :return: An instance :class:`degreedClient.models.content.Course`
        :rtype: :class:`degreedClient.models.content.Course`
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
        Delete a Course by ID.

        :param id: The Course ID
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