import arrow
from attr import attrs, attrib
import attr

@attrs
class ReqLearning(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()
	included = attrib()


@attrs
class LearningsAttribute(object):
	employee_id = attrib()
	assignment_type = attrib()
	due_at = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
