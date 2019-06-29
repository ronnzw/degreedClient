import json

from .compatibility import scrub
from .exceptions import UserNotFoundException
from .models.user import User
from .models.attribute import Attribute


class UserClient(object):
    """ Users API object """
    def __init__(self, client):
        self.client = client

    def all(self, per_page=None, query=None):
        """
        Get all users (will page results out)

        :param per_page: Starting page
        :type  per_page: ``int``

        :param query: Extra query parameters
        :param query: ``dict``

        :return: A list of users
        :rtype: ``list`` of :class:`degreedClient.degreedClient.models.user.User`
        """
        params = {}
        if per_page is not None:
            params['limit'] = per_page

        data = None
        if query is not None:
            data = json.dumps({'q': query})

        users = self.client.get_paged('users', params=params, data=data)
        results = []
        for page in users:
            results.extend([ self._to_user(i) for i in page['data']])
        return results

    def get(self, id):
        """
        Fetch a user by ID.

        :param id: The user id
        :type  id: ``str``

        :return: An instance :class:`degreeedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        user = self.client.get("users/{0}".format(id))
        user_data = user['data']
        return self._to_user(user_data)

    def get_today_learnings(self, id):
        learnings = self.client.get("users/{0}/todays-learning".format(id))
        learnings_data_list = learnings['data']
        if len(learnings_data_list) > 0:
            learnings_dict = learnings_data_list[0]
            learning_details = learnings_dict["attributes"]
        else:
            learning_details = "nothing"

        return learning_details

    def get_user_completions(self, id):
        comp_data = self.client.get("users/{0}/completions".format(id))
        comp_list = comp_data["data"]
        if len(comp_list) > 0:
            comp_dict = comp_list[0]
            comp_details = comp_dict["attributes"]
        else:
            comp_details = "nothing completed yet"
        return comp_details
    
    def get_user_skills(self, id):
        comp_data = self.client.get("users/{0}/user-skills".format(id))
        comp_list = comp_data["data"]
        if len(comp_list) > 0:
            comp_dict = comp_list[0]
            comp_details = comp_dict["attributes"]
        else:
            comp_details = "no user skills yet"
        return comp_details  

    def get_user_certifiable_skills(self, id):
        comp_data = self.client.get("users/{0}/user-skills".format(id))
        comp_list = comp_data["data"]
        if len(comp_list) > 0:
            comp_dict = comp_list[0]
            comp_details = comp_dict["attributes"]
        else:
            comp_details = "no certifiable skills yet"
        return comp_details         

    
    def create(self,
        employee_id,
        first_name,
        last_name,
        organization_email,
        password,
        permission_role,
        profile_visibility,
        full_name=None,
        bio=None,
        login_disabled=False,
        restricted=False,
        real_time_email_notification=False,
        daily_digest_email=False,
        weekly_email_digest=False,):
        """
        Create a user.

        :param name: The users' employee id
        :type  name: ``str``

        :param job_title: The users' first name
        :type  job_title: ``str``

        :param job_title: The users' last name
        :type  job_title: ``str``

        :param job_title: The users' organization email
        :type  job_title: ``str``

        :param job_title: The users' password must be at least 8 characters,
         the must include at least one number and a capital letter.
        :type  job_title: ``str``

        :param job_title: The users' permission role,
        the options are Admin, LearningProfessional, Manager or Member
        :type  job_title: ``str``

        :param job_title: The users' profile visibility 
         the options are Everyone, Organization or Private
        :type  job_title: ``str``

        :param job_title: The users' full name
        :type  job_title: ``str``

        :param job_title: The users' bio
        :type  job_title: ``str``

        :param job_title: login disabled a boolean field
        :type  job_title: ``bool``

        :param job_title: Restricts the user to change certain fields
        :type  job_title: ``bool``

        :param job_title: Optional field
         real time email notifications
        :type  job_title: ``bool``

        :param job_title: Optional daily digest email
        :type  job_title: ``bool``

        :param job_title: Optional
         weekly email digest
        :type  job_title: ``str``        

        :return: An instance :class:`degreedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """


        params = {
            "employee-id": employee_id,
            "first-name": first_name,
            "last-name": last_name,
            "organization-email": organization_email,
            "password": password,
            "permission-role": permission_role,
            "profile-visibility": profile_visibility,
            }
        


        if full_name:
            params['full-name'] = full_name
        if bio:
            params['bio'] = bio
        if login_disabled:
            params['login-disabled'] = login_disabled
        if restricted:
            params['restricted'] = restricted
        if real_time_email_notification:
            params['real-time-email-notification'] = real_time_email_notification
        if daily_digest_email:
            params['daily-digest-email'] = daily_digest_email
        if weekly_email_digest:
            params['weekly-email-digest'] = weekly_email_digest


        user = self.client.post("users", {"data":{"attributes": params}})
        a_user = user['data']
        return self._to_user(a_user)

    def update(self,
        id,
        employee_id=None,
        first_name=None,
        last_name=None,
        organization_email=None,
        password=None,
        permission_role=None,
        profile_visibility=None,
        full_name=None,
        bio=None,
        login_disabled=False,
        restricted=False,
        real_time_email_notification=False,
        daily_digest_email=False,
        weekly_email_digest=False,):
        """
        Create a user.

        :param name: The users' employee id
        :type  name: ``str``

        :param job_title: The users' first name
        :type  job_title: ``str``

        :param job_title: The users' last name
        :type  job_title: ``str``

        :param job_title: The users' organization email
        :type  job_title: ``str``

        :param job_title: The users' password must be at least 8 characters,
         the must include at least one number and a capital letter.
        :type  job_title: ``str``

        :param job_title: The users' permission role,
        the options are Admin, LearningProfessional, Manager or Member
        :type  job_title: ``str``

        :param job_title: The users' profile visibility 
         the options are Everyone, Organization or Private
        :type  job_title: ``str``

        :param job_title: The users' full name
        :type  job_title: ``str``

        :param job_title: The users' bio
        :type  job_title: ``str``

        :param job_title: login disabled a boolean field
        :type  job_title: ``bool``

        :param job_title: Restricts the user to change certain fields
        :type  job_title: ``bool``

        :param job_title: Optional field
         real time email notifications
        :type  job_title: ``bool``

        :param job_title: Optional daily digest email
        :type  job_title: ``bool``

        :param job_title: Optional
         weekly email digest
        :type  job_title: ``str``        

        :return: An instance :class:`degreedClient.degreedClient.models.user.User`
        :rtype: :class:`degreeedClient.degreedClient.models.user.User`
        """
        params = {}
        if employee_id:
            params["employee-id"] = employee_id
        if first_name:
            params["first-name"] = first_name
        if last_name:
            params["last-name"] = last_name
        if organization_email:
            params["organization-email"] = organization_email
        if password:
            params["password"] = password
        if permission_role:
            params["permission-role"] = permission_role
        if profile_visibility:
            params["profile-visibility"] = profile_visibility
        if full_name:
            params['full-name'] = full_name
        if bio:
            params['bio'] = bio
        if login_disabled:
            params['login-disabled'] = login_disabled
        if restricted:
            params['restricted'] = restricted
        if real_time_email_notification:
            params['real-time-email-notification'] = real_time_email_notification
        if daily_digest_email:
            params['daily-digest-email'] = daily_digest_email
        if weekly_email_digest:
            params['weekly-email-digest'] = weekly_email_digest

        user = self.client.patch("users/{0}".format(id), {"data":{"type": "users", "id": id, "attributes": params }})
        a_user = user['data']
        return self._to_user(a_user)

    def delete(self, id):
        """
        Delete a user by ID.

        :param id: The user ID
        :type  id: ``str``

        :return: None
        :rtype: None    
        """
        self.client.delete("users/{0}".format(id))




    def _to_user(self, data):
        scrub(data)

        if "attributes" in data and data["attributes"] is not None:
        	data['attributes'] = { x.replace('-','_'): y
        	for x,y in data['attributes'].items()}
        	data["attributes"] = Attribute(**data["attributes"])
        return User(**data)

