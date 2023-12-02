from models.user import User

def get_user_by_id(id: str):
    if not id:return None
    user = User.query.filter_by(id=id).first()
    return user