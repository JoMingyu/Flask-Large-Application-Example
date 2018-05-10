from bson.objectid import ObjectId
from datetime import datetime
from decimal import Decimal

from mongoengine.base import BaseDocument


def _list_field_to_dict(list_field):
    """
    ListField to [{}, {}, ...] with mongo_to_dict()
    """
    return_data = []

    for item in list_field:
        if isinstance(item, BaseDocument):
            return_data.append(mongo_to_dict(item, []))
        else:
            return_data.append(_field_value_to_python_type(item, True))

    return return_data


def _field_value_to_python_type(data, escape_datetime=False):
    if isinstance(data, datetime):
        return str(data)[:10] if escape_datetime else str(data)
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, list):
        return _list_field_to_dict(data)
    elif isinstance(data, BaseDocument):
        return mongo_to_dict(data, ['_cls'])
    else:
        # dict, str, float, int, ...
        return data


def _extract_field_data(field_value):
    if field_value is None:
        return None
    else:
        return _field_value_to_python_type(field_value, True)


def mongo_to_dict(obj, exclude_fields=list()):
    """
    Convert Document of MongoEngine's instance to dictionary type

    Args:
        obj (BaseDocument): Document of MongoEngine
        exclude_fields (list): Field names for exclude

    Returns:
        dict
    """
    exclude_fields.append('_cls')
    return_data = {}

    if obj is None:
        return None

    document_data_dict = obj._data

    if 'id' not in exclude_fields and 'id' in document_data_dict:
        # EmbeddedDocument doesn't have _id
        return_data['id'] = str(obj.id)

    for k, v in document_data_dict.items():
        if k in exclude_fields:
            continue

        return_data[k] = _extract_field_data(v)

    return return_data
