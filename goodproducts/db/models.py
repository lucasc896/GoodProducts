import datetime
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'
    __sequence_name__ = 'products_product_code_sequence'

    sequence = sa.Sequence(name=__sequence_name__)

    id = sa.Column(sa.Integer,
                   sequence,
                   primary_key=True)

    name = sa.Column(
        'Name',
        sa.String(128),
        nullable=False,
        doc="Name of product")

    price = sa.Column(
        'Price', 
        sa.Numeric(2),
        nullable=False,
        doc="Price of product")
