from flask import request, render_template, flash, redirect, url_for
from .blueprint import user
from .blueprint import product
from models.user import User

#회원가입 페이지 API
@user.route('/form')
def form():
    
    return render_template('user_form.html')


#회원가입 API
@user.route('/signup', methods=['POST'])
def signup():
    form_data = request.form
    
    #비밀번호와 비밀번호 확인이 일치하지 않으면 비밀번호가 같지 않습니다 생성
    if form_data['password'] != form_data['password_confirmation']:
        flash('비밀번호가 같지 않습니다')
        return render_template('user_form.html')
        
    #이미 존재하는 이메일
    if not User.check_email(form_data['email']):
        flash('사용 중인 이메일입니다')
        return render_template('user_form.html')
    
    User.insert_one(form_data)
    
    return redirect(url_for('product.get_products'))