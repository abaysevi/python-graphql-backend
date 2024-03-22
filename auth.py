from db import db
import jwt
from bson import ObjectId

def checkcurrentUser(token):
    if token:
        # Remove the "Bearer " prefix from the token
        token = token.replace("Bearer ", "")
        print(token)
        decoded_token = jwt.decode(token, "secretkey", algorithms=["HS256"])
        print(decoded_token)
        user_id = decoded_token.get("id")
        print(user_id)
        if user_id:
            return db.get_users_collection().find_one({"_id": ObjectId(user_id)})
    print("No token")
    return None