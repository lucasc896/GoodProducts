# GoodProducts

[the beginnings of] a RESTful backend API for an online marketplace. Basic product details are stored in a MYSQL DB instance called 'goodproducts'. An API is provided to interface with the DB.


## Install

This codebase should be ran within a python3 virtual environment. Assuming virtualenvwrapper is used, and python3 installed:

```
cd GoodProducts;
mkvirtualenv -p $(which python3) GoodProducts
pip install -r requirements.txt;
pip install -e .
```

### DB initialization

GoodProducts requires two mysql db instances, 'production' and 'testing'. Login and create then doing:
```
CREATE DATABASE goodproducts;
CREATE DATABASE test_goodproducts_db;
```

Set environement variables GOODPRODUCTS_TEST_DB_URL and GOODPRODUCTS_DB_URL, e.g. for bash:
```
export GOODPRODUCTS_DB_URL='mysql://chrislucas@localhost/goodproducts';
export GOODPRODUCTS_TEST_DB_URL='mysql://chrislucas@localhost/test_goodproducts_db';
```

Initialise both DBs by running the manage-db script with the 'create' option for both, and in addition the 'initialise' option for the production db:

```
# Test db
manage-db -m create

# Prod DB
manage-db -m create -i -d $GOODPRODUCTS_DB_URL
```

### Setup Flask
From the base directory:

```
export FLASK_APP=goodproducts/flask/app.py;
export FLASK_DEBUG=1;
```

`python -m flask run`

Access the API via `http://127.0.0.1:5000/<endpoint>`


## Running tests
Some unit tests are written using pytest. They hit the test mysql db instance, stripping down and rebuilding it for each test.

Test environment requirements are installed using:

`pip install -r requirements-test.txt`

and ran with:

`py.test test -v`


## API info

The following endpoints are currently implemented:

* GET /products – A list of products, names, and prices in JSON format.  
* POST /product – Create a new product using posted form data
* GET /product/{product_id} – Return a single product in JSON format.


## Notes
* have ignored the currency in the Price column (looks OK to do from a brief look at tests.postman)


## TO-DO
* return proper flask.response objects for each request
* strong er type validation for form data