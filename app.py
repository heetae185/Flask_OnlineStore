from flask import Flask, redirect, url_for
from unicodedata import name
from controllers.product import product
from controllers.user import user


app = Flask(__name__)

app.secret_key = 'online_store'

app.register_blueprint(product, url_prefix='/products')
app.register_blueprint(user, url_prefix='/users')

@app.route("/")
def home():
    return redirect(url_for('product.get_products'))

if __name__ == "__main__":
    app.run(debug=True)

