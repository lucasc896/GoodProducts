import os

import ujson

from goodproducts.api import api
from goodproducts.db.manage import get_session
from goodproducts.flask import helpers
from flask import Flask, request, jsonify, make_response
# from wtforms import Form, StringField, DecimalField, validators

app = Flask("goodproducts")

GOODPRODUCTS_DB_URL = os.environ.get('GOODPRODUCTS_DB_URL', 'mysql://root@localhost/goodproducts')
SESSION = get_session(GOODPRODUCTS_DB_URL)


@app.errorhandler(404)
def product_not_found(error=None):
    message = {
            'status': 404,
            'message': 'Product not found: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(404)
def bad_request(error=None):
    message = {
            'status': 404,
            'message': 'Bad request: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/products', methods=['GET'])
def list_all_products():
    return jsonify(api.get_list_of_products(SESSION))


@app.route('/product/<int:productid>', methods=['GET'])
def list_single_product(productid):
    result = api.get_single_product_info(SESSION, productid)
    if result[1] == 200:
        return jsonify(result[0])
    elif result[1] == 404:
        return product_not_found(result[0])
    else:
        return make_response(*result)


@app.route('/product', methods=['POST'])
def add_product():

    if ("multipart/form-data" in request.headers['Content-Type'] 
        or request.headers['Content-Type'] == "application/x-www-form-urlencoded"):


        product_form = helpers.ProductForm(request.form)

        if product_form.validate():
            response = api.add_new_product(SESSION,
                                           product_form.data.get('name'),
                                           product_form.data.get('price'))
        else:
            return bad_request("Invalid Form Data")

    if response:
        return response[0]

    return bad_request("Error. Nothing happened.")


@app.route('/product/<int:productid>', methods=['DELETE'])
def delete_product():
    result = api.delete_single_product(SESSION, productid)
    if result[1] == 200: #check is right code
        return "Product id={} deleted.".format(productid)
    elif result[1] == 204:
        return product_not_found(result[0])
    else:
        return bad_request("Bad times.")