from attr import attrs, attrib


@attrs
class TheView(object):
	id = attrib()
	attributes = attrib()
	links = attrib()
	relationships = attrib()



@attrs
class TheViewAttribute(object):
	url = attrib()
	content_type = attrib()
	content_title = attrib()
	view_count = attrib()

