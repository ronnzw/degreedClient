import arrow
import attr

from attr import attrs, attrib



@attrs
class CertifiableSkill(object):
	id = attrib()
	attributes = attrib()
	links = attrib()


@attrs
class CertifiableSkillAttribute(object):
	name = attrib()
	description = attrib()
	skill_unique_identifier = attrib()
	is_featured = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	visibility = attrib(default=None)
	cost = attrib(default=0)