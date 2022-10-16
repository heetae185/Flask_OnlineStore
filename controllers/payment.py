from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from .blueprint import order
from .blueprint import payment
from .auth import check_login, is_admin, redirect_to_signin_form
from models.user import User
from models.order import Order

# 결제 요청 페이지 API
@payment.route('/request')
def request_payment():
    user = check_login()
    if not user:
        return redirect_to_signin_form()
    
    order_id = request.args.get('order_id') #브라우저에 물음표 붇는 부분
    order = Order.find_one(order_id)
    
    return render_template('payment.html', order=order)



