from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from models.user import User

def check_login():
    if not session.get('user_id'):
        return False
    
    # user 값으로 user가 나오거나 False가 나오게 됨
    user = User.find_one(session['user_id'])
    
    return user

def redirect_to_signin_form():
    flash('로그인이 필요합니다')
    return redirect(url_for('user.signin_form'))

def is_admin():
    user = check_login()
    if not user:
        return False
    return user.get('is_admin', False) #is_admin 있으면 is_admin 반환하고 없으면 False 반환