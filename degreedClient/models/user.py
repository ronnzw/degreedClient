import arrow
import attr

from attr import attrs, attrib


@attrs
class User(object):
    id = attrib()
    attributes = attrib()
    links = attrib()
    relationships = attrib(default=None)
    included = attrib(default=None)