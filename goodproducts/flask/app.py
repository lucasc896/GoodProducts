import os

import ujson

from goodproducts.api import api
from goodproducts.db.manage import get_session
from flask import Flask, request, jsonify
from wtforms import Form, StringField, DecimalField, validators

app = Flask("goodproducts")

GOODPRODUCTS_DB_URL = os.environ.get('GOODPRODUCTS_DB_URL', 'mysql://root@localhost/goodproducts')
SESSION = get_session(GOODPRODUCTS_DB_URL)


class ProductForm(Form):
    """
    WTForm for POST form data for new products
    """
    name = StringField('name', validators=[validators.Length(min=1, max=64), validators.DataRequired()])
    price = DecimalField('price', validators=[validators.NumberRange(min=1.), validators.DataRequired()])


@app.route('/products', methods=['GET'])
def list_all_products():
    return jsonify(api.get_list_of_products(SESSION))


@app.route('/product/<int:articleid>', methods=['GET'])
def list_single_product(articleid):
    return jsonify(api.get_single_product_info(SESSION, articleid))


@app.route('/product', methods=['POST'])
def add_product():
    if request.headers['Content-Type'] == "multipart/form-data":
        # TO-DO: something cool here
        1/0
    elif request.headers['Content-Type'] == "application/x-www-form-urlencoded":
        
        product_form = ProductForm(request.form)

        if product_form.validate():
            response = api.add_new_product(SESSION,
                                           product_form.data.get('name'),
                                           product_form.data.get('price'))
        else:
            # abort
            print("Invalid Form Data")

    if response:
        code, msg = response
        return msg
    return "nothing"
