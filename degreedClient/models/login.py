import arrow
import attr

from attr import attrs, attrib




@attrs
class Login(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class LoginAttribute(object):
	employee_id = attrib()
	logged_in_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)