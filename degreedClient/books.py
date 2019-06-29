import json

from .models.content import ( Content, ContentAttribute, ArticleAttribute,
    Article, BookAttribute, Book)
from .models.user import User
from .compatibility import scrub


class BookClient(object):
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

        books = self.client.get_paged('content/books', params=params, data=data)
        results = []
        for page in books:
            results.extend([ self._to_books(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        book = self.client.get("content/books/{0}".format(id))
        a_book = book['data']
        return self._to_books(a_book)

    def create(self,
    	title,
        external_id,        
        subtitle=None,
        author=None,
        pages=0,
        summary=None,
        obsolete=None,
        publish_date=None,
        language=None,
        i_s_b_n13=None):
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
            "external-id": external_id
            }
        
        if subtitle:
            params['subtitle'] = subtitle
        if author:
            params['author'] = author
        if pages:
            params['pages'] = pages
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if publish_date:
            params['publish-date'] = publish_date
        if language:
            params['language'] = language
        if i_s_b_n13:
            params['i-s-b-n13'] = i_s_b_n13

        book = self.client.post("content/books", {"data":{"attributes": params}})
        a_book = book['data']
        return self._to_books(a_book)

    def update(self,
        id,
        title=None,
        external_id=None,        
        subtitle=None,
        author=None,
        pages=0,
        summary=None,
        obsolete=None,
        publish_date=None,
        language=None,
        i_s_b_n13=None):
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

        if title:
            params['title'] = title
        if external_id:
            params['external-id'] = external_id
        if subtitle:
            params['subtitle'] = subtitle
        if author:
            params['author'] = author
        if pages:
            params['pages'] = pages
        if summary:
            params['summary'] = summary
        if obsolete:
            params['obsolete'] = obsolete
        if publish_date:
            params['publish-date'] = publish_date
        if language:
            params['language'] = language
        if i_s_b_n13:
            params['i-s-b-n13'] = i_s_b_n13

        book = self.client.patch("content/books/{0}".format(id), {"data":{"attributes": params}})
        a_book = book['data']
        return self._to_books(a_book)

    def delete(self, id):
        """
        Delete an book by ID.

        :param id: The book ID
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("content/books/{0}".format(id))

    def _to_books(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = BookAttribute(**data['attributes'])
        return Book(**data)