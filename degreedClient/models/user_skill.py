import arrow
import attr

from attr import attrs, attrib



@attrs
class UserSkill(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class UserSkillAttribute(object):
	employee_id = attrib()
	skill_id = attrib()
	skill_name = attrib()
	certifiable_skill_guid = attrib()
	followed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
