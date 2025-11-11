Quick Start Guide
=================

This guide will help you get started with SheetAlchemy in minutes.

Prerequisites
-------------

Before starting, make sure you have:

1. Installed SheetAlchemy (see :doc:`installation`)
2. Set up Google Sheets API access
3. A Google Sheet with some data

Step 1: Authentication
----------------------

First, authenticate with Google Sheets API using your service account key:

.. code-block:: python

   from sheetalchemy import authenticate

   # Using a key file path
   authenticate(key_path="/path/to/your/service-account-key.json")

Alternatively, you can use an environment variable:

.. code-block:: python

   import os
   os.environ['SHEETALCHEMY_AUTH_KEY_PATH'] = '/path/to/your/key.json'

Step 2: Define Your Model
--------------------------

Create a model that represents a tab in your Google Sheet:

.. code-block:: python

   from sheetalchemy import Model, StringField, IntegerField, BooleanField

   class Users(Model):
       name = StringField(name="Name")
       age = IntegerField(name="Age")
       is_active = BooleanField(name="Active")

       class Meta:
           sheet_name = "My Google Sheet"  # Name of your Google Sheet
           tab_name = "Users"               # Name of the worksheet/tab
           header_index = 1                 # Row number with headers (1-indexed)

Let's break this down:

- **Fields**: Each field represents a column in your sheet
- **name**: The exact column header name in your sheet
- **Meta**: Configuration for connecting to your sheet

Step 3: Query Your Data
------------------------

Now you can query your Google Sheet data using a familiar Django-like syntax:

Get All Records
~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all users
   all_users = Users.manager.filter()
   
   for user in all_users:
       print(f"{user.name}: {user.age} years old")

Filter Records
~~~~~~~~~~~~~~

.. code-block:: python

   # Get active users
   active_users = Users.manager.filter(is_active=True)

   # Get users older than 25
   adult_users = Users.manager.filter(age__gt=25)

   # Multiple conditions (AND operation)
   young_active = Users.manager.filter(age__lt=30, is_active=True)

Get Single Record
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get a specific user
   user = Users.manager.get(name="John Doe")
   print(f"Found: {user.name}, Age: {user.age}")

Step 4: Working with Results
-----------------------------

SheetAlchemy provides convenient methods to work with query results:

.. code-block:: python

   # Get filtered results
   results = Users.manager.filter(is_active=True)

   # Get first result
   first_user = results.first()

   # Get last result
   last_user = results.last()

   # Get specific item by index
   third_user = results.nth(2)

   # Get total count
   count = results.size()
   print(f"Found {count} active users")

   # Iterate through results
   for user in results:
       print(user.name)

Complete Example
----------------

Here's a complete working example:

.. code-block:: python

   from sheetalchemy import Model, StringField, IntegerField, BooleanField, authenticate

   # Step 1: Authenticate
   authenticate(key_path="path/to/service-account-key.json")

   # Step 2: Define Model
   class Users(Model):
       name = StringField(name="Name")
       age = IntegerField(name="Age")
       email = StringField(name="Email")
       is_active = BooleanField(name="Active")

       class Meta:
           sheet_name = "User Management System"
           tab_name = "Users"
           header_index = 1

   # Step 3: Query Data
   
   # Get all active users over 18
   adult_users = Users.manager.filter(age__gte=18, is_active=True)
   
   print(f"Found {adult_users.size()} adult active users:")
   for user in adult_users:
       print(f"  - {user.name} ({user.age}) - {user.email}")
   
   # Get a specific user
   try:
       john = Users.manager.get(name="John Doe")
       print(f"\nJohn's age: {john.age}")
   except Exception as e:
       print(f"User not found: {e}")

   # Get first 5 users
   results = Users.manager.filter()
   for i in range(min(5, results.size())):
       user = results.nth(i)
       print(f"{i+1}. {user.name}")

Example Google Sheet Structure
-------------------------------

Your Google Sheet should have a structure like this:

.. list-table:: Users Tab
   :header-rows: 1
   :widths: 25 15 40 20

   * - Name
     - Age
     - Email
     - Active
   * - John Doe
     - 30
     - john@example.com
     - TRUE
   * - Jane Smith
     - 25
     - jane@example.com
     - TRUE
   * - Bob Johnson
     - 45
     - bob@example.com
     - FALSE

Important Notes:

- The header row should be at the index specified in ``header_index`` (1-indexed)
- Column names in the sheet must match the ``name`` parameter in your fields
- Boolean values can be TRUE/FALSE, true/false, yes/no, 1/0

Next Steps
----------

Now that you understand the basics, explore:

- :doc:`models` - Learn more about model configuration
- :doc:`fields` - Discover all available field types
- :doc:`querying` - Master advanced querying techniques
- :doc:`advanced` - Explore advanced features

Common Patterns
---------------

Filter by Multiple Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # All conditions must be true (AND operation)
   results = Users.manager.filter(
       age__gte=18,
       age__lt=65,
       is_active=True
   )

Case-Insensitive String Matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Contains search (case-insensitive by default with gspread)
   results = Users.manager.filter(name__ct="john")

Range Queries
~~~~~~~~~~~~~

.. code-block:: python

   # Users between 25 and 35 years old
   young_adults = Users.manager.filter(age__gte=25, age__lte=35)

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from sheetalchemy.exceptions import ModelItemException

   try:
       user = Users.manager.get(name="NonExistent User")
   except ModelItemException:
       print("User not found")

   # Check for field validation errors
   user = Users.manager.get(name="John")
   errors = user.get_errors()
   if errors:
       print(f"Validation errors: {errors}")
