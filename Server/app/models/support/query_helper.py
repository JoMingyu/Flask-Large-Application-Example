from app.models.support.mongo_helper import mongo_to_dict


def find_as_listed_dict(model, exclude_fields=list(), **kwargs):
    """
    Find model's data as listed dict.

    :param model: Document of MongoEngine
    :param exclude_fields: field names for exclude
    :param kwargs: Additional options when querying

    :rtype: list
    """
    return [mongo_to_dict(obj, exclude_fields) for obj in model.objects(kwargs)]


def find_as_dict_with_object_id(model, object_id, exclude_fields=list(), **kwargs):
    """
    Find model's document with id.

    :param model: Document of MongoEngine
    :param object_id: ObjectId for find
    :param exclude_fields: field names for exclude
    :param kwargs: Additional options when querying

    :rtype: dict
    """
    if len(object_id) != 24:
        raise ValueError

    obj = model.objects(kwargs, id=object_id).first()
    if not obj:
        raise ValueError

    return mongo_to_dict(obj, exclude_fields)


def delete_with_object_id(model, object_id, **kwargs):
    """
    Delete model's document with id.

    :param model: Document of MongoEngine
    :param object_id: ObjectId for delete
    """
    if len(object_id) != 24:
        raise ValueError

    obj = model.objects(kwargs, id=object_id).first()
    if not obj:
        raise ValueError

    obj.delete()
