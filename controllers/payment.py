from flask import jsonify, request, render_template, flash, redirect, url_for, session, make_response
from .blueprint import user
from .blueprint import product
from .blueprint import order
from .blueprint import payment
from .auth import check_login, is_admin, redirect_to_signin_form
from models.user import User
from models.order import Order
from models.payment import Payment
import requests, json

# 결제 요청 페이지 API
@payment.route('/request')
def request_payment():
    user = check_login()
    if not user:
        return redirect_to_signin_form()
    
    order_id = request.args.get('order_id') #브라우저에 물음표 붇는 부분
    order = Order.find_one(order_id)
    
    return render_template('payment.html', order=order)


# 결제 완료 및 주문 상태 업데이트 API
@payment.route('/complete', methods=['POST'])
def complete_payment():
    user = check_login()
    if not user:
        return redirect_to_signin_form()
    
    request_data = request.get_json()
    imp_uid = request_data['imp_uid']
    merchant_uid = request_data['merchant_uid']
    
    # 결제가 실제로 완료가 되었는지 확인 => 결제애 대한 정보를 저장 => 주문 document status 완료 상태로 업데이트
    IAMPORT_GET_TOKEN_URL = "https://api.iamport.kr/users/getToken"
    data = {
        "imp_key" : "6674716100886453",
        "imp_secret" : "GzC5L1f9zhjUcnl9qJwH3Bbg5J1PMeELWijoBS8tJgxsFFvQ2HRY8Aw6bCJDuraKJGx9ZUb03YQDtYZv"
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(IAMPORT_GET_TOKEN_URL, headers=headers, data=json.dumps(data))
    res = res.json()
    #엑세스 토큰을 access_token에 저장
    access_token = res['response']['access_token']
    
    iamport_get_payment_data_url = f'https://api.iamport.kr/payments/{imp_uid}'
    headers = {'Authorization': access_token}
    
    res = requests.get(iamport_get_payment_data_url, headers=headers)
    res = res.json()
    payment_data = res['response']
    
    # 실제 결제 금액과 상품 정보가 맞으면 정상적으로 결제 완료된 것
    order = Order.find_one(merchant_uid)
    if not order:
        return jsonify({'message': '존재하지 않는 주문입니다.'})
    
    if payment_data and payment_data['amount'] == order['product']['price']:
        status = 'success'
        # 결제 정보 저장
        Payment.insert_one(order, payment_data, status)
    else:
        status = 'fail'
        Payment.insert_one(order, payment_data, status)
        return jsonify({'message': '비정상적인 결제입니다.'})

    # Order에 status 업데이트
    status = {'status': 'complete'}
    Order.update_one(merchant_uid, status)
    
    return jsonify({'order_id': merchant_uid, 'message': 'success'})


# 결제 성공 페이지
@payment.route('/success')
def success():
    order_id = request.args.get('order_id')    # location.herf = `/payments/success?order_id=${order_id}`
    
    return render_template('payment_complete.html', order_id=order_id)