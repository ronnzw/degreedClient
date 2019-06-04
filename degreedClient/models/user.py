from attr import attrs, attrib


@attrs
class User(object):
    id = attrib()
    attributes = attrib()
    links = attrib()
