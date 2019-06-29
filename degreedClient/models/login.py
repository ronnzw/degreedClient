import arrow
from attr import attrs, attrib
import attr



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