import factory

from factory.alchemy import SQLAlchemyModelFactory
from goodproducts.db import models, manage


SESSION = manage.get_test_session()


class ProductsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Products
        sqlalchemy_session = SESSION

    id = factory.Sequence(int)
    name = factory.Sequence(str)
    price = factory.Sequence(float)
