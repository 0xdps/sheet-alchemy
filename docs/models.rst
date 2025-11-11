Models
======

Models in SheetAlchemy are Python classes that represent tabs in your Google Sheets. They define the structure, validation rules, and behavior of your data.

Defining Models
---------------

Basic Model
~~~~~~~~~~~

A basic model requires at minimum:

- One or more field definitions
- A ``Meta`` class with configuration

.. code-block:: python

   from sheetalchemy import Model, StringField, IntegerField

   class Users(Model):
       name = StringField(name="Name")
       age = IntegerField(name="Age")

       class Meta:
           sheet_name = "My Google Sheet"
           tab_name = "Users"
           header_index = 1

Meta Configuration
------------------

The ``Meta`` class configures how the model connects to your Google Sheet.

Required Settings
~~~~~~~~~~~~~~~~~

.. py:attribute:: sheet_name
   :type: str

   The exact name of your Google Sheet document.

.. py:attribute:: tab_name
   :type: str

   The name of the worksheet/tab within the sheet.

.. py:attribute:: header_index
   :type: int

   The row number (1-indexed) where column headers are located.

Optional Settings
~~~~~~~~~~~~~~~~~

.. py:attribute:: load_policy
   :type: LoadPolicy
   :value: LoadPolicy.LAZY

   Controls when data is loaded from Google Sheets.

   - ``LoadPolicy.LAZY``: Load data when first accessed (default)
   - ``LoadPolicy.INIT``: Load data immediately when model is defined

Example with All Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sheetalchemy import Model, LoadPolicy, StringField

   class Products(Model):
       name = StringField(name="Product Name")
       sku = StringField(name="SKU")

       class Meta:
           sheet_name = "Inventory Management"
           tab_name = "Products"
           header_index = 1
           load_policy = LoadPolicy.INIT

Load Policies
-------------

LAZY Loading (Default)
~~~~~~~~~~~~~~~~~~~~~~~

Data is loaded from Google Sheets only when you first query it:

.. code-block:: python

   class Users(Model):
       name = StringField(name="Name")

       class Meta:
           sheet_name = "My Sheet"
           tab_name = "Users"
           header_index = 1
           load_policy = LoadPolicy.LAZY  # Default

   # No data loaded yet
   # Data is loaded here when first query executes
   users = Users.manager.filter()

**Advantages:**

- Faster application startup
- Saves API calls if model is never queried
- Good for models accessed conditionally

**Use when:**

- You have many models
- Not all models are always used
- API quota is a concern

INIT Loading
~~~~~~~~~~~~

Data is loaded immediately when the model class is defined:

.. code-block:: python

   class Users(Model):
       name = StringField(name="Name")

       class Meta:
           sheet_name = "My Sheet"
           tab_name = "Users"
           header_index = 1
           load_policy = LoadPolicy.INIT

   # Data is already loaded by this point

**Advantages:**

- Fail fast if sheet is unavailable
- Consistent query performance
- Better for frequently accessed data

**Use when:**

- Model is always queried
- You want to catch connection errors early
- Query performance consistency is important

Model Manager
-------------

Every model automatically gets a ``manager`` attribute for querying data.

Manager Methods
~~~~~~~~~~~~~~~

.. py:method:: filter(**kwargs)

   Filter records based on field values.

   .. code-block:: python

      Users.manager.filter(age__gt=25, is_active=True)

.. py:method:: get(**kwargs)

   Get a single record. Raises ``ModelItemException`` if not found or multiple found.

   .. code-block:: python

      user = Users.manager.get(name="John Doe")

.. py:method:: reload_model()

   Reload data from Google Sheets.

   .. code-block:: python

      Users.manager.reload_model()

.. py:method:: initialise_model()

   Manually load data for lazy-loaded models.

   .. code-block:: python

      Users.manager.initialise_model()

Working with Model Instances
-----------------------------

Accessing Fields
~~~~~~~~~~~~~~~~

.. code-block:: python

   user = Users.manager.get(name="John")
   
   # Access field values
   print(user.name)
   print(user.age)

Model Methods
~~~~~~~~~~~~~

.. py:method:: to_json()

   Convert model instance to JSON-serializable dictionary.

   .. code-block:: python

      user = Users.manager.get(name="John")
      data = user.to_json()
      # {'name': 'John', 'age': 30}

.. py:method:: get_errors()

   Get dictionary of field validation errors.

   .. code-block:: python

      user = Users.manager.get(name="John")
      errors = user.get_errors()
      if errors:
          print(f"Validation errors: {errors}")

.. py:method:: get_raw_data()

   Get the raw row data from Google Sheets.

   .. code-block:: python

      user = Users.manager.get(name="John")
      raw = user.get_raw_data()

.. py:method:: get_raw_value(field_name)

   Get the raw value for a specific field before transformation.

   .. code-block:: python

      user = Users.manager.get(name="John")
      raw_age = user.get_raw_value("age")

Model Inheritance
-----------------

You can create base models with common fields:

.. code-block:: python

   from sheetalchemy import Model, StringField, DateField

   class BaseModel(Model):
       created_at = DateField(name="Created", format=DateField.MM_DD_YYYY)
       updated_at = DateField(name="Updated", format=DateField.MM_DD_YYYY)

       class Meta:
           abstract = True  # Not supported yet, define in each model

   class Users(Model):
       name = StringField(name="Name")
       created_at = DateField(name="Created", format=DateField.MM_DD_YYYY)

       class Meta:
           sheet_name = "My Sheet"
           tab_name = "Users"
           header_index = 1

Note: Abstract base models are not yet implemented. For now, define common fields in each model.

Multiple Models, Same Sheet
---------------------------

You can have multiple models pointing to different tabs in the same sheet:

.. code-block:: python

   class Users(Model):
       name = StringField(name="Name")

       class Meta:
           sheet_name = "Company Data"
           tab_name = "Users"
           header_index = 1

   class Products(Model):
       name = StringField(name="Product")

       class Meta:
           sheet_name = "Company Data"
           tab_name = "Products"
           header_index = 1

Best Practices
--------------

1. **Clear Model Names**

   Use descriptive names that match your domain:

   .. code-block:: python

      class CustomerOrder(Model):  # Good
      class CO(Model):              # Bad - unclear

2. **Consistent Field Naming**

   Match Python conventions for attributes:

   .. code-block:: python

      first_name = StringField(name="First Name")  # Good
      FirstName = StringField(name="First Name")   # Bad

3. **Document Your Models**

   Add docstrings:

   .. code-block:: python

      class Users(Model):
          """
          Represents user data from the Users tab.
          
          Fields:
              name: User's full name
              email: User's email address
              is_active: Whether user is currently active
          """
          name = StringField(name="Name")
          email = StringField(name="Email")
          is_active = BooleanField(name="Active")

4. **Choose Appropriate Load Policy**

   - Use ``LAZY`` for models that may not be queried
   - Use ``INIT`` for frequently accessed models

5. **Handle Missing Data**

   Use field defaults for optional columns:

   .. code-block:: python

      phone = StringField(
          name="Phone",
          allow_empty_or_null=True,
          default_val=""
      )

Common Patterns
---------------

Configuration Model
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class Config(Model):
       key = StringField(name="Key")
       value = StringField(name="Value")

       class Meta:
           sheet_name = "App Configuration"
           tab_name = "Config"
           header_index = 1
           load_policy = LoadPolicy.INIT  # Load immediately

   # Access configuration
   config = {c.key: c.value for c in Config.manager.filter()}

Lookup Tables
~~~~~~~~~~~~~

.. code-block:: python

   class Countries(Model):
       code = StringField(name="Code")
       name = StringField(name="Country Name")

       class Meta:
           sheet_name = "Reference Data"
           tab_name = "Countries"
           header_index = 1
           load_policy = LoadPolicy.INIT

   # Create lookup dictionary
   country_map = {c.code: c.name for c in Countries.manager.filter()}

Next Steps
----------

- :doc:`fields` - Learn about field types
- :doc:`querying` - Master querying techniques
- :doc:`advanced` - Explore advanced features
