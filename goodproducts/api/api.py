# import ujson

from goodproducts.db import models


def product_to_dict(product):
    """
    takes a goodproducts.db.models.Products object, returning a dict of
    relevant params
    """
    keys = ['id', 'name', 'price']
    return {key:product.__dict__.get(key) for key in keys}
    # return ujson.dumps(d)


def add_new_product(session, name, price):
    if product_exists(session, name, price):
        print("Product (name: {}, price: {}) already exists in db".format(
            name, price))
        return (301, 'Product already exists')

    # add product


def get_list_of_products(session):
    products_query = session.query(models.Products)
    # TO-DO: set?
    return [product_to_dict(prod) for prod in products_query]


def product_exists(session):
    pass    