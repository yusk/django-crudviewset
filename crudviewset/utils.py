def get_field_names(cls):
    return [f.name for f in cls._meta.fields]


def get_editable_field_names(cls):
    return [f.name for f in cls._meta.fields if f.editable]
