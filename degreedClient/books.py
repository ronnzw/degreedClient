import json

from .models.content import BookAttribute, Book
from .compatibility import scrub


class BookClient(object):
    """ Book Content API. """

    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, next_id=None):
        """
        Gets all books.

        :param per_page: Amount of books per page
        :type  per_page: ``str``

        :param next_id: Supplied to retrieve the next batch of articles
        :type  query: ``str``

        :return: A list of books
        :rtype: ``list`` of :class:`degreedClient.models.content.Book`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if next_id is not None:
            data = json.dumps({'next': next_id })

        books = self.client.get_paged('content/books', params=params, data=data)
        results = []
        for page in books:
            results.extend([ self._to_books(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a book by ID.

        :param id: The book id
        :type  id: ``str``

        :return: An instance :class:`degreedClient.models.content.Book`
        :rtype: :class:`degreedClient.models.content.Book`
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
        Create a Book.

        :param title: The book title, is required
        :type  title: ``str``

        :param external_id: The book's external id, is required
        :type  external_id: ``str``

        :param subtitle: The book's subtitle
        :type  subtitle: ``str``

        :param author: The book's author
        :type  author: ``str``

        :param pages: Amount of pages
        :type  pages: ``int``

        :param summary: Short summary of the book
        :type  summary: ``str`` 

        :param obsolete: If the book should be marked as obsolete
        :type  obsolete: ``bool``

        :param publish_date: Date that the book has been published
        :type  publish_date: ``str``

        :param language:    Language of the book
        :type  language: ``str``

        :param i_s_b_n13: Short summary of the book
        :type  i_s_b_n13: ``str``                                      

        :return: An instance :class:`degreedClient.models.content.Book`
        :rtype: :class:`degreedClient.models.content.Book`
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
        Update a Book.

        :param id: The ID of the book to update
        :type  id: ``str``        

        :param title: The book title, is required
        :type  title: ``str``

        :param external_id: The book's external id, is required
        :type  external_id: ``str``

        :param subtitle: The book's subtitle
        :type  subtitle: ``str``

        :param author: The book's author
        :type  author: ``str``

        :param pages: Amount of pages
        :type  pages: ``int``

        :param summary: Short summary of the book
        :type  summary: ``str`` 

        :param obsolete: If the book should be marked as obsolete
        :type  obsolete: ``bool``

        :param publish_date: Date that the book has been published
        :type  publish_date: ``str``

        :param language:    Language of the book
        :type  language: ``str``

        :param i_s_b_n13: Short summary of the book
        :type  i_s_b_n13: ``str``                                      

        :return: An instance :class:`degreedClient.models.content.Book`
        :rtype: :class:`degreedClient.models.content.Book`
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