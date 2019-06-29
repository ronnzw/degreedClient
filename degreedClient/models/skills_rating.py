import arrow
from attr import attrs, attrib
import attr


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
	rated_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)