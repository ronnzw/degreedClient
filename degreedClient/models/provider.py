import arrow
import attr

from attr import attrs, attrib



@attrs
class Provider(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()


@attrs
class ProviderAttribute(object):
	follower_employee_id = attrib()
	following_employee_id = attrib()
	followed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class SpecificProvider(object):
	id = attrib()
	attributes = attrib()
	links = attrib()


@attrs
class SpecificProviderAttribute(object):
	name = attrib()
	url = attrib()


@attrs
class ProviderLicence(object):
	id = attrib()
	attributes= attrib()
	links = attrib()
	relationships = attrib()


@attrs
class ProviderLicenceAttribute(object):
	employee_id = attrib()
	is_enabled = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


