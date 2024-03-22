
from ariadne import MutationType, QueryType
from db import db
import bcrypt
import jwt
from bson import ObjectId

query = QueryType()
mutation = MutationType()

@query.field("users")
def resolve_users(*_):
    users = list(db.get_users_collection().find())
    for user in users:
        user["id"] = str(user.pop("_id"))
    return users


@query.field("currentUser")
def resolve_current_user(_, info):
    token = info.context["request"].headers.get('authorization')
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



@query.field("allPosts")
def resolve_all_posts(_, info):
    return list(db.get_posts_collection().find())

@mutation.field("createUser")
def resolve_create_user(_, info, input):
    hashed_password = bcrypt.hashpw(input["password"].encode(), bcrypt.gensalt())
    user_data = {
        "name": input["name"],
        "email": input["email"],
        "password": hashed_password.decode("utf-8"),
        "role": input["role"]
    }
    result = db.get_users_collection().insert_one(user_data)
    user = db.get_users_collection().find_one({"_id": result.inserted_id})
    user["id"] = str(user.pop("_id"))
    return user

@mutation.field("createPost")
def resolve_create_post(_, info, input):
    current_user = info.context.get("current_user")
    if current_user:
        print("__________________________found it!____________________________")
        post_data = {
            "post_media_url": input["post_media_url"],
            "post_title": input["post_title"],
            "post_descri": input["post_descri"],
            "user_id": current_user["id"],
            "created_date": "current date",  # You need to update this with the actual current date
            "updated_date": None  # You need to update this with the actual current date
        }
        result = db.get_posts_collection().insert_one(post_data)
        post = db.get_posts_collection().find_one({"_id": result.inserted_id})
        post["id"] = str(post.pop("_id"))
        return post
    print("there is no current user")
    return None

@mutation.field("login")
def resolve_login(_, info, input):
    user = db.get_users_collection().find_one({"email": input["email"]})
    if user and bcrypt.checkpw(input["password"].encode(), user["password"].encode()):
        token = jwt.encode({"id": str(user["_id"])}, "secretkey", algorithm="HS256")
        return {"token": token, "error": None}
    return {"token": None, "error": "Invalid credentials"}
