from models.user import User
from sqlalchemy.orm import class_mapper
def get_user_by_id(id: str):
    if not id:return None
    user = User.query.filter_by(id=id).first()
    return user


def object_as_dict(obj):
    # Convert the object to a dictionary
    return {col.name: getattr(obj, col.name) for col in class_mapper(obj.__class__).mapped_table.c}