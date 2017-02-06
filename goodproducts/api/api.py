import decimal

import sqlalchemy as sa

from goodproducts.db import models


def product_to_dict(product):
    """
    takes a goodproducts.db.models.Products object, returning a dict of
    relevant params
    """
    keys = ['id', 'name', 'price']
    # import pdb; pdb.set_trace()
    d = {key:product.__dict__.get(key) for key in keys}
    # hack to get around json serializing Decimal type
    if isinstance(d.get('price'), decimal.Decimal):
        d['price'] = float(d.get('price'))
    return d



def add_new_product(session, name, price):
    """
    Add new product object to db
    - will return 204 if product already exists (even though mysql will silently ignore
      duplicates)
    """

    # TO-DO: type validation - done in WTForm?

    if product_exists(session, name):
        return ("Product ('{}', {}) already exists in db".format(
            name, price), 204)

    try:
        product_obj = models.Products(name=name,
                                      price=price)
        session.add(product_obj)
        session.commit()
    except sa.exc.DataError as exc:
        return ("DB error when adding product ('{}', {})".format(
            name, price), 400)

    product = session.query(models.Products).filter(models.Products.name == name).one()

    return ("Product ('{}', {}) added with id={}.".format(
        product.name, product.price, product.id), 201)


def get_list_of_products(session):
    """
    return list of all products in the db
    """
    products_query = session.query(models.Products)
    # TO-DO: set?
    return [product_to_dict(prod) for prod in products_query]


def product_exists(session, name):
    """
    return boolean if a product already exists with 'name' in db
    TO-DO: could also check something about the price - direct float comparison isn't
           the one
    """
    result = session.query(models.Products).filter(models.Products.name == name)
    return bool(result.count())


def get_single_product_info(session, prod_id):
    result = session.query(models.Products).filter(models.Products.id == prod_id)
    if result.count() == 1:
        return (product_to_dict(result.one()), 200)
    elif result.count() == 0:
        return ("id={} does not exist in the DB.".format(prod_id), 404)
    else:
        return ("Product id={} returns multiple products DB. That's mental.".format(prod_id), 204)


def delete_single_product(session, prod_id):
    # do delete
    # no need to check if exists

    # check if item is deleted?
    return ("", 200)