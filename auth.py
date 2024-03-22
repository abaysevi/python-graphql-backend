from db import db
import jwt
from bson import ObjectId

def checkcurrentUser(token):
    if token:
        # Remove the "Bearer " prefix from the token
        token = token.replace("Bearer ", "")
        decoded_token = jwt.decode(token, "secretkey", algorithms=["HS256"])
        user_id = decoded_token.get("id")
    if user_id:
        user_data = db.get_users_collection().find_one({"_id": ObjectId(user_id)})
        user_data["id"] = str(user_data.pop("_id"))  # Convert ObjectId to string
        return user_data
    print("No token")
    return None