Querying
========

SheetAlchemy provides a Django-inspired querying interface for filtering and retrieving data from Google Sheets.

Manager Methods
---------------

The model ``manager`` provides methods for querying data.

filter()
~~~~~~~~

Returns an iterator of records matching the criteria.

.. code-block:: python

   # Get all records
   all_users = Users.manager.filter()

   # Filter by field value
   active_users = Users.manager.filter(is_active=True)

   # Multiple conditions (AND)
   young_active = Users.manager.filter(age__lt=30, is_active=True)

get()
~~~~~

Returns a single record. Raises exception if not found or multiple found.

.. code-block:: python

   user = Users.manager.get(name="John Doe")

Working with Results
--------------------

The ``filter()`` method returns an iterator with helpful methods:

.. code-block:: python

   results = Users.manager.filter(is_active=True)

   # Get first item
   first = results.first()

   # Get last item
   last = results.last()

   # Get nth item (0-indexed)
   third = results.nth(2)

   # Get count
   count = results.size()

   # Iterate
   for user in results:
       print(user.name)

   # Reset iterator
   results.reset()

Query Operators
---------------

Field Lookups
~~~~~~~~~~~~~

Use double underscore notation for field lookups:

Comparison Operators
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Exact match (default)
   Users.manager.filter(age=25)

   # Less than
   Users.manager.filter(age__lt=30)

   # Less than or equal
   Users.manager.filter(age__lte=30)

   # Greater than
   Users.manager.filter(age__gt=18)

   # Greater than or equal
   Users.manager.filter(age__gte=18)

String Operators
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Exact match
   Users.manager.filter(name="John Doe")

   # Contains (substring)
   Users.manager.filter(name__ct="John")

Complex Queries
---------------

Multiple Conditions
~~~~~~~~~~~~~~~~~~~

All conditions in a single ``filter()`` call are combined with AND logic:

.. code-block:: python

   # Age between 25 and 35, and active
   results = Users.manager.filter(
       age__gte=25,
       age__lte=35,
       is_active=True
   )

Chaining Filters
~~~~~~~~~~~~~~~~

Note: Currently, filter results cannot be chained. Apply all conditions in one call:

.. code-block:: python

   # All conditions in one filter
   results = Users.manager.filter(age__gt=18, is_active=True)

Error Handling
--------------

Handle Missing Records
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sheetalchemy.exceptions import ModelItemException

   try:
       user = Users.manager.get(name="NonExistent")
   except ModelItemException as e:
       print(f"User not found: {e}")

Check for Empty Results
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   results = Users.manager.filter(age__gt=100)
   
   if results.size() == 0:
       print("No results found")

Best Practices
--------------

1. **Use get() for unique records**
2. **Use filter() for multiple records**
3. **Cache results if querying multiple times**
4. **Handle exceptions appropriately**

Next Steps
----------

- :doc:`advanced` - Advanced querying techniques
- :doc:`models` - Learn about models
