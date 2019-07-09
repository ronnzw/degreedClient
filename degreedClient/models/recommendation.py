import arrow
import attr

from attr import attrs, attrib



@attrs
class Recommendation(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()
	included = attrib()


@attrs
class RecoAttribute(object):
	employee_id = attrib()
	recipient_employee_id = attrib()
	status = attrib()
	recommended_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)