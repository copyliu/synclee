from django.contrib.auth.models import User

from synclee.relationships.models import RelationshipStatus


def relationship_exists(from_user, to_user, status_slug='following'):
    status = RelationshipStatus.objects.by_slug(status_slug)
    if status.from_slug == status_slug:
        return from_user.relationships.exists(to_user, status)
    elif status.to_slug == status_slug:
        return to_user.relationships.exists(from_user, status)
    else:
        return from_user.relationships.symmetrical_exists(to_user, status)

def extract_user_field(model):
    for field in model._meta.fields + model._meta.many_to_many:
        if field.rel and field.rel.to == User:
            return field.name
    for rel in model._meta.get_all_related_many_to_many_objects():
        if rel.model == User:
            return rel.var_name

def positive_filter(qs, user_qs, user_lookup=None):
    if not user_lookup:
        user_lookup = extract_user_field(qs.model)

    if not user_lookup:
        return qs.none() # default to returning none

    query = {'%s__in' % user_lookup: user_qs}

    qs = qs.filter(**query).distinct()
    return qs

def negative_filter(qs, user_qs, user_lookup=None):
    if not user_lookup:
        user_lookup = extract_user_field(qs.model)

    if not user_lookup:
        return qs # default to returning all

    query = {'%s__in' % user_lookup: user_qs}

    qs = qs.exclude(**query).distinct()
    return qs
