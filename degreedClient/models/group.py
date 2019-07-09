import arrow
import attr

from attr import attrs, attrib



@attrs
class Group(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class GroupAttribute(object):
	name = attrib()
	description = attrib()
	privacy = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)

