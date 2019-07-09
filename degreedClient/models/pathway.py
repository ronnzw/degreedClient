import arrow
import attr

from attr import attrs, attrib



@attrs
class Pathway(object):
	id  = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class PathwayAttribute(object):
	title = attrib()
	summary = attrib()
	visibility = attrib()
	sections = attrib(default=None)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class Tag(object):
	id = attrib()
	attributes = attrib()
	links = attrib()


@attrs
class TagAttribute(object):
	tag = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class Collaborator(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class CollaboratorAttribute(object):
	employee_id = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)

@attrs
class Follower(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class FollowerAttribute(object):
	employee_id = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)

@attrs
class GrpPathway(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class GrpPathwayAttribute(object):
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)