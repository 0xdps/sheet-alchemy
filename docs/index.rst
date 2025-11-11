SheetAlchemy Documentation
==========================

**SheetAlchemy** is a Python library that provides an Object-Relational Mapping (ORM) interface for Google Sheets. It allows developers to interact with Google Sheets data using Python objects and Django-like query syntax.

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.8+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Features
--------

- **Model-Based Approach**: Define Python classes that represent Google Sheets tabs
- **Rich Field Types**: Support for String, Integer, Date, Boolean, Decimal, List, and Custom fields
- **Django-Style Queries**: Familiar filtering and querying with field lookups (``__lt``, ``__gt``, ``__ct``, etc.)
- **Data Validation**: Built-in type validation and error handling
- **Load Policies**: Configure eager (``INIT``) or lazy (``LAZY``) data loading
- **Data Transformation**: Automatic cleaning of common spreadsheet issues
- **Authentication Management**: Seamless Google Sheets API authentication

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install sheetalchemy

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from sheetalchemy import Model, StringField, IntegerField, authenticate

   # Authenticate with Google Sheets
   authenticate(key_path="/path/to/service-account-key.json")

   # Define your model
   class Users(Model):
       name = StringField(name="Name")
       age = IntegerField(name="Age")

       class Meta:
           sheet_name = "My Google Sheet"
           tab_name = "Users"
           header_index = 1

   # Query your data
   users = Users.manager.filter(age__gt=25)
   for user in users:
       print(f"{user.name}: {user.age}")

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   authentication
   models
   fields
   querying
   advanced

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/model
   api/fields
   api/manager
   api/exceptions
   api/transformers

.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   tutorials/getting_started
   tutorials/field_types
   tutorials/querying
   tutorials/advanced_usage

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   examples
   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
