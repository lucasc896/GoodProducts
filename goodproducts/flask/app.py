import os

import ujson

from goodproducts.api import api
from goodproducts.db.manage import get_session
from flask import Flask, request, jsonify
from wtforms import Form, StringField, DecimalField, validators

app = Flask("goodproducts")

GOODPRODUCTS_DB_URL = os.environ.get('GOODPRODUCTS_DB_URL', 'mysql://root@localhost/goodproducts')
SESSION = get_session(GOODPRODUCTS_DB_URL)


@app.route('/products', methods=['GET'])
def list_all_products():
    return jsonify(api.get_list_of_products(SESSION))


@app.route('/product/<int:articleid>', methods=['GET'])
def list_single_product():
    pass


@app.route('/product', methods=['POST'])
def add_product():
    print(request.headers)
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        new_product_data = ujson.dumps(request.json)
    elif request.headers['Content-Type'] == "multipart/form-data":
        print(request.form)
        1/0
    elif request.headers['Content-Type'] == "application/x-www-form-urlencoded":

    print("nothing")
    return ""