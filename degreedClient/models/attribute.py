from attr import attrs, attrib


@attrs
class Attribute(object):
    employee_id = attrib()
    first_name = attrib()
    last_name = attrib()
    full_name = attrib(default=None)
    organization_email = attrib(default=None)
    personal_email = attrib(default=None)
    profile_visibility = attrib(default=None)
    bio = attrib(default=None)
    location = attrib(default=None)
    profile_image_url = attrib(default=None)
    login_disabled = attrib(default=False)
    restricted = attrib(default=False)
    permission_role =attrib(default=None)
    real_time_email_notification = attrib(default=False)
    daily_digest_email = attrib(default=False)
    weekly_digest_email = attrib(default=False)
    created_at = attrib(default=None)