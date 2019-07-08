from attr import attrs, attrib


@attrs
class SearchTerm(object):
	id = attrib()
	attributes = attrib()
	links = attrib()



@attrs
class SearchTermAttribute(object):
	search_term = attrib()
	count = attrib()