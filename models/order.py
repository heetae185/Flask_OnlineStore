from datetime import datetime
from .mongodb import conn_mongodb
from bson import ObjectId


class Order():
    @staticmethod
    def insert_one(product, form, user):
        db = conn_mongodb()
        db.orders.insert_one({
            'status': 'pending',
            'product': product,
            'postcode': form['postcode'],
            'address': form['address'],
            'detail_address': form['detail_address'],
            'extra_address': form.get('extra_address', ''), #값이 없으면 ''를 넣음
            'user_name': form['user_name'],
            'user_phone': form['user_phone'],
            'user': user,
            'created_at': int(datetime.now().timestamp()),
            'updated_at': int(datetime.now().timestamp())
        })
        
    @staticmethod
    def find():
        db = conn_mongodb()
        orders = db.orders.find({})
        
        return orders
    
    @staticmethod
    def find_one(order_id):
        db = conn_mongodb()
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        
        return order