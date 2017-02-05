import sqlalchemy as sa

from goodproducts.db import models


def product_to_dict(product):
    """
    takes a goodproducts.db.models.Products object, returning a dict of
    relevant params
    """
    keys = ['id', 'name', 'price']
    return {key:product.__dict__.get(key) for key in keys}
    # d = {key:product.__dict__.get(key) for key in keys}
    # return ujson.dumps(d)


def add_new_product(session, name, price):
    """
    Add new product object to db
    - will return 204 if product already exists (even though mysql will silently ignore
      duplicates)
    """

    # TO-DO: type validation - done in WTForm?

    if product_exists(session, name):
        return (204, "Product ('{}', {}) already exists in db".format(
            name, price))

    try:
        product_obj = models.Products(name=name,
                                      price=price)
        session.add(product_obj)
        session.commit()
    except sa.exc.DataError as exc:
        return (400, "DB error when adding product ('{}', {})".format(
            name, price))

    return (201, "Product ('{}', {}) added.".format(
        name, price))


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
