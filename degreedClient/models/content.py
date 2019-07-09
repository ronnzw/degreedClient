import arrow
import attr

from attr import attrs, attrib



@attrs
class Content(object):
	id = attrib()
	attributes = attrib(default=None)
	links = attrib(default=None)


@attrs
class ContentAttribute(object):
	content_type = attrib()
	external_id = attrib(default=None)
	title = attrib(default=None)
	summary = attrib(default=None)
	url = attrib(default=None)
	_format = attrib(default=None)
	is_obsolete = attrib(default=False)
	image_url = attrib(default=None)
	language = attrib(default=None)
	duration = attrib(default=None)
	duration_type = attrib(default=None)
	provider = attrib(default=None)
	is_internal = attrib(default=False)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class Article(object):
	id = attrib()
	attributes = attrib(default=None)
	links = attrib(default=None)


@attrs
class ArticleAttribute(object):
	title = attrib()
	summary = attrib()
	url = attrib()
	_format = attrib(default=None)
	obsolete = attrib(default=None)
	image_url = attrib(default=None)
	language = attrib(default=None)
	num_words = attrib(default=0)
	provider_code = attrib(default=None)
	external_id = attrib(default=None)
	publish_date = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class Book(object):
	id = attrib()
	attributes = attrib(default=None)
	links = attrib(default=None)


@attrs
class BookAttribute(object):
	title = attrib()
	subtitle = attrib()
	authors = attrib()
	pages = attrib()
	summary = attrib()
	image_url = attrib(default=None)	
	obsolete = attrib(default=None)
	publish_date = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	language = attrib(default=None)
	external_id = attrib(default=None)
	i_s_b_n13 = attrib(default=None)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)	
	provider_code = attrib(default=None)


@attrs
class Video(object):
	id = attrib()
	attributes = attrib(default=None)
	links = attrib(default=None)


@attrs
class VideoAttribute(object):
	provider_code = attrib()
	external_id = attrib()
	title = attrib()
	duration = attrib()
	duration_type = attrib()
	summary = attrib()
	url = attrib()
	obsolete = attrib(default=None)
	image_url = attrib(default=None)
	language = attrib(default=None)
	publish_date = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)


@attrs
class Course(object):
	id = attrib()
	attributes = attrib(default=None)
	links = attrib(default=None)


@attrs
class CourseAttribute(object):
	provider_code = attrib()
	external_id = attrib()
	title = attrib()
	summary = attrib()
	url = attrib()
	obsolete = attrib()
	image_url = attrib()
	language = attrib()
	duration = attrib()
	duration_type = attrib()
	cost_units = attrib()
	cost_unit_type = attrib()
	_format = attrib()
	difficulty = attrib()
	video_url = attrib()
	created_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
	modified_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)

	











