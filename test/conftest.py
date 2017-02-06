import pytest

from goodproducts.db.manage import create_all, drop_all, get_test_session
from goodproducts.db import models


@pytest.fixture(scope='function')
def session(request):
    session = get_test_session()

    drop_all()
    create_all()

    def teardown():
        session.rollback()
        session.close_all()
        drop_all()
        session.close()

    request.addfinalizer(teardown)
    return get_test_session()


# @pytest.fixture(scope='function')
# def add_product(session, product_dict):
#     product_object = models.Products(name=test_product.get("name"),
#                                      price=test_product.get("price"))
#     session.add(product_object)
#     session.flush()