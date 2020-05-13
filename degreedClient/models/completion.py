import arrow
import attr

from attr import attrs, attrib



@attrs
class Completion(object):
    id = attrib()
    attributes = attrib()
    links = attrib()
    relationships = attrib(default=None)
    included = attrib(default=None)


@attrs
class CompletionAttribute(object):
    employee_id = attrib()
    completed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
    added_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
    points_earned = attrib(default=0)
    is_verified = attrib(default=False)
    rating = attrib(default=0)
    access_method = attrib(default=None)


@attrs
class CompletionCreationAttributes(object):
    user_id = attrib()
    user_identifier_type = attrib()
    content_id = attrib()
    content_id_type = attrib()
    content_type = attrib()
    completed_at = attr.ib(converter=attr.converters.optional(arrow.get), default=None)
    is_verified = attrib(default=False)
    questions_correct = attrib(default=0)
    percentile = attrib(default=0)
    duration = attrib(default=0)
    involvement_level = attrib(default=None)


@attrs
class Relationships(object):
    user = attrib()


@attrs
class RelationshipsData(object):
    id = attrib()



@attrs
class RelationshipsProvider(object):
    id = attrib()
    type_ = attrib()


@attrs
class RelationshipsUser(object):
    id = attrib()
    type_ = attrib()


@attrs
class Included(object):
    id = attrib()
    attributes = attrib()
    links = attrib()


@attrs
class IncludeAttributes(object):
    content_type = attrib()
    url = attrib()
    title = attrib()
    provider = attrib()

