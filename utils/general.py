from models.user import User
from sqlalchemy.orm import class_mapper
from enum import Enum
def get_user_by_id(id: str):
    if not id:return None
    user = User.query.filter_by(id=id).first()
    return user


def object_as_dict(obj):
    # Convert the object to a dictionary
    result = {}
    for col in class_mapper(obj.__class__).mapped_table.c:
        value = getattr(obj, col.name)
        # Handle Enums by getting their values
        if isinstance(value, Enum):
            result[col.name] = value.value
        else:
            result[col.name] = value
    return result