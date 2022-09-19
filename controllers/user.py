from flask import request, render_template, flash, redirect, url_for, session
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


#로그인 페이지 API
@user.route('/signin')  #주소가 같아도 방식이 다르면 다른 API라고 인식함
def signin_form():
    return render_template('user_signin.html')


#로그인 API
@user.route('/signin', methods=['POST'])
def signin():
    form_data = request.form
    #이메일, 패스워드 받아서 로그인 가능 여부 가늠
    user = User.sign_in(form_data)
    
    if not user:
        flash('이메일 주소 또는 비밀번호를 확인해주세요.')
        return render_template('user_signin.html')
    else:
        #세션 이용
        session['user_id'] = str(user['_id'])
        return redirect(url_for('product.get_products'))
    

#로그아웃
@user.route('/signout')
def signout():
    #세션 정보 없애면 로그아웃 됨
    session.pop('user_id', None)
    return redirect(url_for('product.get_products'))