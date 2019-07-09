import arrow
import attr

from attr import attrs, attrib


@attrs
class UserFollower(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class UserFollowersAttribute(object):
	follower_employee_id = attrib()
	following_employee_id = attrib()
	followed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)