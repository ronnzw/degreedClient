import arrow
import attr

from attr import attrs, attrib



@attrs
class Completion(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib(default=None)
	included = attrib(default=None)


@attrs
class CompletionAttribute(object):
	employee_id = attrib()
	completed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	added_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	points_earned = attrib(default=0)
	is_verified = attrib(default=False)
	rating = attrib(default=0)
	access_method = attrib(default=None)


@attrs
class NewCompletionAttribute(object):
	user_id = attrib()
	user_identifier_type = attrib()
	content_id = attrib()
	content_id_type = attrib()
	content_type = attrib()
	completed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)