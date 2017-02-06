import pytest
import ujson

from goodproducts.api import api
from goodproducts.db import factories, models
from test import TEST_PRODUCTS


def test_list_all_products(session):

    # TO-DO: could make adding test products a fixture?
    for product in TEST_PRODUCTS:
        factories.ProductsFactory(name=product.get("name"),
                                  price=product.get("price"))

    session.commit()

    api_result = api.get_list_of_products(session)

    assert len(api_result) == 4

    for api_prod in api_result:
        # check has an assigned id value
        assert api_prod.get("id", None) is not None 
        
        # remove auto-incremented id value for comparison
        api_prod.pop("id")
        assert api_prod in TEST_PRODUCTS


def test_product_exists(session):
    test_product = TEST_PRODUCTS[0]
    product_object = models.Products(name=test_product.get("name"),
                                     price=test_product.get("price"))
    session.add(product_object)
    session.flush()

    result = session.query(models.Products)
    assert result.count() == 1
    assert result[0].name == test_product.get("name")
    assert result[0].price == test_product.get("price")



    assert api.product_exists(session,
                              test_product.get("name"))


def test_add_new_product(session):
    test_product = TEST_PRODUCTS[0]

    api_result = api.add_new_product(session,
                                     test_product.get("name"),
                                     test_product.get("price"))

    assert api_result[1] == 201

    result = session.query(models.Products)

    assert result.count() == 1

    assert result[0].name == test_product.get("name")
    assert result[0].price == test_product.get("price")


def test_add_new_product_already_exists(session):
    test_product = TEST_PRODUCTS[0]
    product_object = models.Products(name=test_product.get("name"),
                                     price=test_product.get("price"))
    session.add(product_object)
    session.flush()

    result = api.add_new_product(session,
                                 test_product.get("name"),
                                 test_product.get("price"))

    assert result[1] == 204


def test_add_new_product_db_error(session):
    result = api.add_new_product(session,
                                 'chris',
                                 'not a price')
    assert result[1] == 400


def test_get_single_product_info(session):
    test_product = TEST_PRODUCTS[0]
    product_object = models.Products(name=test_product.get("name"),
                                     price=test_product.get("price"))
    session.add(product_object)
    session.flush()

    result = session.query(models.Products).filter(models.Products.name == test_product.get("name"))
    
    new_prod_id = result.one().id

    api_result = api.get_single_product_info(session, new_prod_id)

    assert api_result[1] == 200
    assert api_result[0].get("name") == test_product.get("name")
    assert api_result[0].get("price") == test_product.get("price")


def test_delete_single_product(session):
    assert True
