import os

import ujson

from goodproducts.api import api
from goodproducts.db.manage import get_session
from flask import Flask, request, jsonify, make_response
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


@app.errorhandler(404)
def product_not_found(error=None):
    message = {
            'status': 404,
            'message': 'Product not found: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/products', methods=['GET'])
def list_all_products():
    return jsonify(api.get_list_of_products(SESSION))


@app.route('/product/<int:articleid>', methods=['GET'])
def list_single_product(articleid):
    result = api.get_single_product_info(SESSION, articleid)
    if result[1] == 200:
        return jsonify(result[0])
    elif result[1] == 404:
        return product_not_found(result[0])
    else:
        return make_response(*result)


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
        return response[0]

    return make_response(400, "nothing happened. oops.")
