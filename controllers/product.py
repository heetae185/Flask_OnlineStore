from flask import request, render_template
from .blueprint import product
from models.product import Product
from werkzeug.utils import secure_filename
from datetime import datetime
import os


@product.route('/form') #GET은 디폴트
def form():
    return render_template('product_form.html') #form 주소로 요청을 하면 html파일을 반환해준다는 내용

#상품 등록 API
@product.route('/regist', methods=['POST'])
def regist():
    #전달받은 상품 정보
    form_data = request.form
    thumbnail_img = request.files.get('thumbnail_img')
    detail_img = request.files.get('detail_img')
    thumbnail_img_url = _upload_file(thumbnail_img)
    detail_img_url = _upload_file(detail_img)
    #저장하는 일
    Product.insert_one(form_data, thumbnail_img_url, detail_img_url)
    
    return "상품 등록 API입니다."


def _upload_file(img_file):
    timestamp = str(datetime.now().timestamp())
    filename = timestamp + '_' + secure_filename(img_file.filename)
    image_path = f'./static/uploads'
    os.makedirs(image_path, exist_ok=True)
    img = os.path.join(image_path, filename)
    img_file.save(img)
    
    return f'/static/uploads/' + filename