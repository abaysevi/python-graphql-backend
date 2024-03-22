from pymongo import MongoClient
from decouple import config

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_users_collection(self):
        return self.db["users"]

    def get_posts_collection(self):
        return self.db["posts"]
    
    def get_products_collection(self):
        return self.db['products']
    
    def get_cart_collection(self):
        return self.db['cart']

    def get_sales_collection(self):
        return self.db['sales']


conn_str = config('DB_LINK')
db = Database(conn_str, "adrina_test")
