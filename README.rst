****************
Asset Management
****************

|Build_Status| |Coverage_Status|

.. |Build_Status| image:: https://circleci.com/gh/AccentDesign/asset_management.svg?style=svg
   :target: https://circleci.com/gh/AccentDesign/asset_management
.. |Coverage_Status| image:: http://img.shields.io/coveralls/AccentDesign/asset_management/master.svg
   :target: https://coveralls.io/r/AccentDesign/asset_management?branch=master

Description
***********

Bare bones starter project complete with the following

- Email authentication
- Login, password reset, password change
- Karma CSS

Getting Started
***************

1, Clone the repo::

    git clone https://github.com/AccentDesign/asset_management.git


2, Docker & Python

Build the container::

    docker-compose build

Up the container, this will also run migrations for you::

    docker-compose up

Create yourself a superuser::

    docker-compose exec app bash
    python manage.py createsuperuser --email=admin@example.com --first_name=Admin --last_name=User


Run python migrations manually::

    docker-compose exec app bash
    python manage.py migrate


Ready!!
*******

The container is ready at http://<docker host ip>:8000/ and a mail server ready at http://<docker host ip>:1080/


Testing
*******

To see the test results and coverage report run::

   docker-compose exec app bash
   make test

The html coverage report is visible in the browser by looking at the htmlcov/index.html once the tests have run.


Styles
******

npm install::

   npm install

build css::

   npm run watch-css
