import pytest

from goodproducts.db import factories, models
from test import TEST_PRODUCT_NAMES


def test_products_table_basic(session):

    for product_name in TEST_PRODUCT_NAMES:
        factories.ProductsFactory(name=product_name)

    session.commit()

    query = session.query(models.Products)

    assert query.count() == 2

    for product in query.all():
        assert product.name in TEST_PRODUCT_NAMES
