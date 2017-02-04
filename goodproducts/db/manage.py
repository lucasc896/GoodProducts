"""This code is heavily taken from a third party codebase"""
import os
import sys

import sqlalchemy as sa

from goodproducts.db import models
from sqlalchemy.orm import sessionmaker

_TEST_SESSION = None

GOODPRODUCTS_TEST_DB_URL = os.environ.get('GOODPRODUCTS_TEST_DB_URL', 'mysql://root@localhost/test_goodproducts_db')


def get_session(url):
    """Return a non scoped database session
    """
    Session = sessionmaker()
    engine = sa.create_engine(url)
    Session.configure(bind=engine)
    return Session()


def get_test_session(url=GOODPRODUCTS_TEST_DB_URL):
    if _TEST_SESSION is None:
        global _TEST_SESSION
        engine = sa.create_engine(url)
        _TEST_SESSION = sessionmaker(bind=engine)()

    return _TEST_SESSION


def _get_medatada(url=GOODPRODUCTS_TEST_DB_URL):
    engine = sa.create_engine(url)
    models.Base.metadata.bind = engine
    return models.Base.metadata


def create_all(url=GOODPRODUCTS_TEST_DB_URL):
    _get_medatada(url).create_all()


def drop_all(url=GOODPRODUCTS_TEST_DB_URL):
    md = _get_medatada(url)
    session = get_test_session(url)
    for table in reversed(md.sorted_tables):
        try:
            session.execute(table.delete())
        except Exception as exc:
            pass

    session.commit()


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Create or destroy the needed tables')
    parser.add_argument('-m', '--mode',
                        choices=('create', 'drop'),
                        default='create',
                        help='Create or drop the tables')

    parser.add_argument('-d', '--dburl',
                        help='SQLAlchemy URL',
                        default=GOODPRODUCTS_TEST_DB_URL)

    return parser.parse_args()


def main():
    args = parse_arguments()

    def _confirm(msg):
        out = input("This would {} on url {}? [y/N] ".format(msg, args.dburl))
        if out != 'y':
            sys.exit(1)

    if args.mode == 'create':
        _confirm("create new tables")
        create_all(args.dburl)

    elif args.mode == 'drop':
        _confirm("drop new tables")
        drop_all(args.dburl)

    print("All good!")


if __name__ == '__main__':
    main()
