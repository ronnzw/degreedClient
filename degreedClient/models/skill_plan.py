import arrow
import attr

from attr import attrs, attrib



@attrs
class SkillPlan(object):
	id = attrib()
	attributes = attrib()
	links = attrib()


@attrs
class SkillPlanAttribute(object):
	name = attrib()
	description = attrib()
	visibility = attrib()
	sections = attrib(default=None)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class SkillFollower(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class SkillFollowerAttribute(object):
	employee_id = attrib()
	enrolled_at = attrib()
	is_primary_plan = attrib()
