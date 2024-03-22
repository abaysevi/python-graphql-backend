
from ariadne import MutationType, QueryType
from db import db
import bcrypt
import jwt
from bson import ObjectId
from auth import checkcurrentUser
from datetime import datetime

query = QueryType()
mutation = MutationType()


@query.field("allProducts")
def resolve_all_products(obj, info):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        products=list(db.get_products_collection().find())
        print(products)
        for product in products:
            product['id']=str(product.pop("_id"))
        return products
    return None

@query.field("cart")
def resolve_cart(obj,info):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        cart=list(db.get_cart_collection().find())
        print(cart)
        for cartitem in cart:
            cartitem['id']=str(cartitem.pop("_id"))
        return cart
    return None


@query.field("sales")
def resolve_sales(obj,info):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        sales=list(db.get_sales_collection().find())
        print(sales)
        for sale in sales:
            sale['id']=str(sale.pop("_id"))
        return sales
    return None


@query.field("users")
def resolve_users(*_):
    users = list(db.get_users_collection().find())
    print(users)
    for user in users:
        print(user  )
        user["id"] = str(user.pop("_id"))
    return users

@query.field("currentUser")
def resolve_current_user(_, info):
    token = info.context["request"].headers.get('authorization')
    user=checkcurrentUser(token)
    print(user)
    return user

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


@mutation.field("login")
def resolve_login(_, info, input):
    user = db.get_users_collection().find_one({"email": input["email"]})
    if user and bcrypt.checkpw(input["password"].encode(), user["password"].encode()):
        token = jwt.encode({"id": str(user["_id"])}, "secretkey", algorithm="HS256")
        return {"token": token, "error": None}
    return {"token": None, "error": "Invalid credentials"}


@mutation.field("addProduct")
def resolve_add_product(_, info, input):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        product_data = {
            "productName": input["productName"],
            "productPrice": input["productPrice"],
            "uniqueCode": input.get("uniqueCode"),
            "tax": input.get("tax"),
            "createdAt": datetime.now().isoformat()  
        }
        result = db.get_products_collection().insert_one(product_data)
        product = db.get_products_collection().find_one({"_id": result.inserted_id})
        product["id"] = str(product.pop("_id"))
        return product
    else:
        raise Exception("Unauthorized. Please log in.")

@mutation.field("addToCart")
def resolve_add_to_cart(_, info, input):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        cart_item_data = {
            "productName": input["productName"],
            "productPrice": input["productPrice"],
            "uniqueCode": input.get("uniqueCode"),
            "tax": input.get("tax"),
            "quantity": input["quantity"],
            "createdAt": datetime.now().isoformat()  # You need to update this with the actual current date
        }
        result = db.get_cart_collection().insert_one(cart_item_data)
        cart_item = db.get_cart_collection().find_one({"_id": result.inserted_id})
        cart_item["id"] = str(cart_item.pop("_id"))
        return cart_item
    else:
        raise Exception("Unauthorized. Please log in.")

@mutation.field("addToSale")
def resolve_add_to_sale(_, info, input):
    token = info.context["request"].headers.get('authorization')
    if checkcurrentUser(token):
        sale_data = {
            "cartItems": input["cartItems"],
            "totalAmount": input["totalAmount"],
            "paymentOption": input["paymentOption"],
            "createdAt": datetime.now().isoformat()  # You need to update this with the actual current date
        }
        result = db.get_sales_collection().insert_one(sale_data)
        sale = db.get_sales_collection().find_one({"_id": result.inserted_id})
        sale["id"] = str(sale.pop("_id"))
        return sale
    else:
        raise Exception("Unauthorized. Please log in.")
