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
        assert api_prod.get('id', None) is not None 
        
        # remove auto-incremented id value for comparison
        api_prod.pop('id')
        assert api_prod in TEST_PRODUCTS

