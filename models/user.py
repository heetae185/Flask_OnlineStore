from datetime import datetime
from .mongodb import conn_mongodb
from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash    #각각 password 암호화, 암호화된 password 체크

class User():
    @staticmethod
    def insert_one(form_data):
        db = conn_mongodb()
        #비밀번호 해시 생성
        password_hash = generate_password_hash(form_data['password'])
        db.users.insert_one({
            'email': form_data['email'],
            'password': password_hash,
            'created_at': int(datetime.now().timestamp()),
            'updated_at': int(datetime.now().timestamp())
    })
        
    def check_email(email):
        db = conn_mongodb()
        user = db.users.find_one({'email': email})
        
        return False if user else True
    
    def sign_in(login_data):
        db = conn_mongodb()
        user = db.users.find_one({'email': login_data['email']})
        
        if not user:
            return False
        if not check_password_hash(user['password'], login_data['password']):
            return False
        
        return user
            
        
        
    