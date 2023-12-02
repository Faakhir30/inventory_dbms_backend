import jwt
from jwt.exceptions import ExpiredSignatureError
import os
secret_key = os.getenv("SECRET_KEY")
from utils.general import get_user_by_id

def token_required_test(authorization: str):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    if not token:
        return None

    try:
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if not data:return None
        current_user = get_user_by_id(data.get("id"))
        return current_user
    except ExpiredSignatureError:
        return None
    except Exception as e:
        print("Exception at auth middleware: ", e)
        return None