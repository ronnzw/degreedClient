import json

from .models.content import Content, ContentAttribute, ArticleAttribute, Article
from .models.user import User
from .compatibility import scrub


class ArticleClient(object):
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

        articles = self.client.get_paged('content/articles', params=params, data=data)
        results = []
        for page in articles:
            results.extend([ self._to_article(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        article = self.client.get("content/articles/{0}".format(id))
        article_data = article['data']
        return self._to_article(article_data)

    def create(self,
    	external_id,
    	title,
    	url,
    	num_words,   	   	
    	summary=None,
    	image_url=None):
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
            "url": url,
            "num-words": num_words,
            }
        
        if summary:
            params['summary'] = summary
        if image_url:
            params['image-url'] = image_url

        article = self.client.post("content/articles", {"data":{"attributes": params}})
        an_article = article['data']
        return self._to_article(an_article)

    def update(self,
    	id,
    	external_id=None,
    	title=None,
    	url=None,
    	num_words=0,   	   	
    	summary=None,
    	image_url=None):
        """
        Can contain any of the values as the Create A New Article

        :param name: id of the article, is required
        :type  name: ``str``

        :param name: The article's external id
        :type  name: ``str``

        :param job_title: The article's title
        :type  job_title: ``str``

        :param job_title: The article's url
        :type  job_title: ``str``

        :param job_title: The article's number of words
        :type  job_title: ``int``

        :param job_title: The article's summary
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
            params["external-id"] = external_id
        if title:
            params["title"] = title
        if url:
            params["url"] = url
        if num_words:
            params["num-words"] = num_words
        if summary:
            params['summary'] = summary
        if image_url:
            params['image-url'] = image_url

        article = self.client.patch("content/articles/{0}".format(id), {"data":{"attributes": params}})
        an_article = article['data']
        return self._to_article(an_article)

    def delete(self, id):
        """
        Delete an article by ID.

        :param id: The article ID
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("content/articles/{0}".format(id))

    def _to_article(self, data):
        scrub(data)
        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data['attributes'] = ArticleAttribute(**data['attributes'])
        return Article(**data)