Advanced Usage
==============

This guide covers advanced SheetAlchemy features and patterns.

Custom Transformers
-------------------

Create custom data transformation functions:

.. code-block:: python

   def clean_phone_number(value):
       """Remove non-digit characters from phone numbers."""
       return ''.join(c for c in str(value) if c.isdigit())

   phone = StringField(
       name="Phone",
       post_transform=[clean_phone_number]
   )

Model Reload
------------

Reload data from Google Sheets:

.. code-block:: python

   # Reload model data
   Users.manager.reload_model()

   # Now queries will use fresh data
   users = Users.manager.filter()

Performance Optimization
------------------------

Load Policy Selection
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # For frequently accessed data
   class Config(Model):
       class Meta:
           load_policy = LoadPolicy.INIT

   # For conditionally accessed data  
   class AuditLog(Model):
       class Meta:
           load_policy = LoadPolicy.LAZY

Best Practices
--------------

1. Use appropriate load policies
2. Cache query results when possible
3. Handle validation errors gracefully
4. Reload data when sheet updates are expected

Next Steps
----------

- :doc:`/api/model` - Complete API reference
- :doc:`quickstart` - Review basics
