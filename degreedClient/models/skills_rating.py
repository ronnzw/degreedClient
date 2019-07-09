import arrow
import attr

from attr import attrs, attrib



@attrs
class SkillRating(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()



@attrs
class SkillRatingAttribute(object):
	employee_id = attrib()
	skill_name = attrib()
	rating = attrib()
	rating_type = attrib()
	certifiable_skill_guid = attrib()
	rated_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)