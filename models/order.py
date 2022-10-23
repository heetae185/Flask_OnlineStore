from datetime import datetime
from .mongodb import conn_mongodb
from bson import ObjectId


class Order():
    @staticmethod
    def insert_one(product, form, user):
        db = conn_mongodb()
        new_order_doc = db.orders.insert_one({
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
        
        return new_order_doc.inserted_id    # inserted_id 하면 생성되었을 때 고유 번호 리턴해줌
        
        
    @staticmethod
    def find(match={}): # match가 없으면 {}가 들어감, 즉 status가 complete면 match에 들어감 
        db = conn_mongodb()
        orders = db.orders.find(match)
        
        return orders
    
    @staticmethod
    def find_one(order_id):
        db = conn_mongodb()
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        
        return order
    
    
    @staticmethod
    def update_one(order_id, status):
        db = conn_mongodb()
        db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': status})