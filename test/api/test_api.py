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

    api.add_new_product(session,
                        test_product.get("name"),
                        test_product.get("price"))

    result = session.query(models.Products)

    assert result.count() == 1

    assert result[0].name == test_product.get("name")
    assert result[0].price == test_product.get("price")
