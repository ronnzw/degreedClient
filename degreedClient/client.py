# -*- coding: utf-8 -*-

"""Main module."""
import json
import requests
import urllib.parse as urlparse

from .articles import ArticleClient
from .books import BookClient
from .certifiable_skills import CertifiableSkillClient
from .completions import CompletionClient
from .content import ContentClient
from .courses import CourseClient
from .exceptions import DegreedApiException 
from .groups import GroupClient
from .logins import LoginClient
from .pathways import PathwayClient
from .providers import ProviderClient
from .recommendations import RecommendationClient
from .required_learnings import RequiredLearningsClient
from .skills_plan import SkillPlanClient
from .skills_ratings import SkillRatingClient
from .users import UserClient
from .user_skills import UserSkillClient
from .user_followers import UserFollowersClient
from .videos import VideoClient





class DegreedApiClient(object):

    """Main API client."""


    """
    Set the default results per page. Max 100
    """
    results_per_page = 100

    def __init__(self, client_id, client_secret, scope=None, proxy=None, skip_ssl_validation=False):
        """
        Instantiate a new API client

        :param client_id: client_id, e.g. 'a123b456cd789' (request from degreed)
        :type  client_id: ``str``

        :param client_secret: client_secret (request from degreed)
        :type  client_secret: ``str``

        :param scope: The scope of the access rights eg 'users:read'
        :type  scope: ``str``        

        :param proxy: The proxy to connect through
        :type  proxy: ``str``

        :param skip_ssl_validation: Skip SSL validation
        :type  skip_ssl_validation: ``bool``
        """
        self._client_id = client_id

        self._client_secret = client_secret

        #self.base_url = "https://api.degreed.com/api/v2"
        self.base_url = "https://api.betatest.degreed.com/api/v2"
        #self.token_req_url  = "https://degreed.com/oauth/token"
        self.token_req_url  = "https://betatest.degreed.com/oauth/token"
        self.session = requests.Session()

        self.scope_list = 'users:read'

        if scope == None:
            self.scope = self.scope_list
        else:
            self.scope = scope

        if proxy:
            self.session.proxies = {"https": proxy}
        if skip_ssl_validation:
            self.session.verify = False

        payload = {
            'grant_type': "client_credentials",
            'client_id': '{0}'.format(self._client_id),
            'client_secret':'{0}'.format(self._client_secret),
            'scope': '{0}'.format(self.scope),
        }

        headers = {
            'content-type': "application/x-www-form-urlencoded",
            }

        self.response = self.session.post(self.token_req_url, data=payload, headers=headers)
        self.access_data = self.response.json()
        try:
            self.expiry_time = self.access_data['expires_in']
            self.access_token = self.access_data['access_token']
            self._refresh_token = self.access_data['refresh_token']

            if self.expiry_time <= 50:
                payload = {
                    'grant_type': "refresh_token",
                    'refresh_token': self._refresh_token,
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                    'scope': 'users:read'
                }

                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                }

                self.response = session.post(token_req_url, data=payload, headers=headers)
                self.access_data = self.response.json()
                self.access_token = self.access_data['access_token']  
            else:
                pass

            self.session.headers.update(
                {
                    "Authorization": "Bearer {0}".format(self.access_token),
                }
            )
        except KeyError:
            pass

        self._users = UserClient(self)
        self._content = ContentClient(self)
        self._article = ArticleClient(self)
        self._book = BookClient(self)
        self._video = VideoClient(self)
        self._course = CourseClient(self)
        self._group = GroupClient(self)
        self._completion = CompletionClient(self)
        self._login = LoginClient(self)
        self._pathway = PathwayClient(self)
        self._recommendation = RecommendationClient(self)
        self._learnings = RequiredLearningsClient(self)
        self._userfollower = UserFollowersClient(self)
        self._provider = ProviderClient(self)
        self._skillplan = SkillPlanClient(self)
        self._userskill = UserSkillClient(self)
        self._certifiableskill = CertifiableSkillClient(self)
        self._skillrating = SkillRatingClient(self)

    def get(self, uri, params=None, data=None):
        try:
            if params:
                if "limit" not in params:
                    params["limit"] = self.results_per_page
            else:
                params = {"limit": self.results_per_page}
            result = self.session.get(
                "{0}/{1}".format(self.base_url, uri), params=params, data=data
            )
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text, uri)

    def get_paged(self, uri, params=None, data=None):
        try:
            page = None
            end = False
            while not end:
                result = self.get(uri, params={"next": page}, data=data)
                links_dict = result["links"]
                if 'next' in links_dict:
                    next_page_link = links_dict["next"]
                    yield result
                    if next_page_link:
                        parsed = urlparse.urlparse(next_page_link)
                        next_id = urlparse.parse_qs(parsed.query)["next"]
                        next_page = str(next_id[0])
                        page = next_page
                    else:
                        end = True
                else:
                    break

        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text, uri)

    def post(self, uri, data=None):
        try:
            result = self.session.post("{0}/{1}".format(self.base_url, uri), json=data)
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text)

    def patch(self, uri, data=None):
        try:
            result = self.session.patch("{0}/{1}".format(self.base_url, uri), json=data)
            result.raise_for_status()

            return result.json()
        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text)
            
    def put(self, uri, data=None):
        try:
            result = self.session.put("{0}/{1}".format(self.base_url, uri), json=data)
            result.raise_for_status()
            if result.text:
                return result.json()
        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text)

    def delete(self, uri):
        try:
            result = self.session.delete("{0}/{1}".format(self.base_url, uri))
            result.raise_for_status()
        except requests.HTTPError as e:
            raise DegreedApiException(e.response.text)

    @property
    def users(self):
        """
        Users

        :rtype: :class:`degreedClient.users.UserClient`
        """
        return self._users

    @property
    def content(self):
        """
        Learning Content

        :rtype: :class:`degreedClient.content.ContentClient`
        """
        return self._content

    @property
    def article(self):
        """
        Learning Articles

        :rtype: :class:`degreedClient.articles.ArticleClient`
        """
        return self._article

    @property
    def book(self):
        """
        Learning Books

        :rtype: :class:`degreedClient.books.BookClient`
        """        
        return self._book
    
    @property
    def video(self):
        """
        Learning Videos

        :rtype: :class:`degreedClient.videos.VideoClient`
        """         
        return self._video
    @property
    def course(self):
        """
        Learning Courses

        :rtype: :class:`degreedClient.courses.CourseClient`
        """                 
        return self._course
    
    @property
    def group(self):
        """
        Groups

        :rtype: :class:`degreedClient.groups.GroupClient`
        """          
        return self._group

    @property
    def completion(self):
        """
        Completion

        :rtype: :class:`degreedClient.completions.CompletionClient`
        """          
        return self._completion

    @property
    def login(self):
        """
        Login

        :rtype: :class:`degreedClient.logins.LoginClient`
        """             
        return self._login

    @property
    def pathway(self):
        """
        Pathways

        :rtype: :class:`degreedClient.pathways.PathwayClient`
        """          
        return self._pathway
    
    @property
    def recommendation(self):
        """
        Recommendation

        :rtype: :class:`degreedClient.recommendations.RecommendationClient`
        """
        return self._recommendation

    @property
    def learnings(self):
        """
        Required Learnings

        :rtype: :class:`degreedClient.required_learnings.RequiredLearningsClient`
        """        
        return self._learnings

    @property
    def userfollower(self):
        """
        User Followers

        :rtype: :class:`degreedClient.user_followers.UserFollowersClient`
        """        
        return self._userfollower
    
    @property
    def provider(self):
        """
        Provider

        :rtype: :class:`degreedClient.providers.ProviderClient`
        """          
        return self._provider
    
    @property
    def skillplan(self):
        """
        Skill Plans

        :rtype: :class:`degreedClient.skills_plan.SkillPlanClient`
        """        
        return self._skillplan

    @property
    def userskill(self):
        """
        User Skills

        :rtype: :class:`degreedClient.user_skills.UserSkillClient`
        """        
        return self._userskill

    @property
    def certifiableskill(self):
        """
        Certifiable Skills

        :rtype: :class:`degreedClient.certifiable_skills.CertifiableSkillClient`
        """        
        return self._certifiableskill


    @property
    def skillrating(self):
        """
        Skill Ratings

        :rtype: :class:`degreedClient.skills_ratings.SkillRatingClient`
        """        
        return self._skillrating
    
    
    
    
###############################################################
#.       Continue from here...if new modules are set
###############################################################























