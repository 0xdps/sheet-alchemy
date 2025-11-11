Fields
======

Fields define how data from Google Sheets columns is mapped, validated, and transformed in your Python models.

Field Types
-----------

StringField
~~~~~~~~~~~

Maps string/text data from Google Sheets.

.. code-block:: python

   from sheetalchemy import StringField

   name = StringField(
       name="Name",
       allow_empty_or_null=True,
       default_val="Unknown"
   )

**Query Operators:**

- ``=`` (default): Exact match
- ``__ct``: Contains (substring search)

.. code-block:: python

   # Exact match
   Users.manager.filter(name="John Doe")
   
   # Contains search
   Users.manager.filter(name__ct="John")

IntegerField
~~~~~~~~~~~~

Maps integer/number data.

.. code-block:: python

   from sheetalchemy import IntegerField

   age = IntegerField(
       name="Age",
       allow_empty_or_null=False
   )

**Query Operators:**

- ``=`` (default): Equal to
- ``__lt``: Less than
- ``__lte``: Less than or equal to
- ``__gt``: Greater than
- ``__gte``: Greater than or equal to

.. code-block:: python

   Users.manager.filter(age=25)           # Equal to 25
   Users.manager.filter(age__lt=30)       # Less than 30
   Users.manager.filter(age__gte=18)      # Greater than or equal to 18

DecimalField
~~~~~~~~~~~~

Maps floating-point/decimal numbers.

.. code-block:: python

   from sheetalchemy import DecimalField

   price = DecimalField(
       name="Price",
       allow_empty_or_null=True,
       default_val=0.0
   )

Same query operators as IntegerField.

BooleanField
~~~~~~~~~~~~

Maps boolean/checkbox data.

.. code-block:: python

   from sheetalchemy import BooleanField

   is_active = BooleanField(name="Active")

**Accepted Values:**

- True: ``"true"``, ``"t"``, ``"yes"``, ``"y"``, ``"ok"``, ``"1"`` (case-insensitive)
- False: Everything else

.. code-block:: python

   Users.manager.filter(is_active=True)
   Users.manager.filter(is_active=False)

DateField
~~~~~~~~~

Maps date data with format specification.

.. code-block:: python

   from sheetalchemy import DateField

   # Predefined formats
   dob = DateField(name="DOB", format=DateField.MM_DD_YYYY)
   created = DateField(name="Created", format=DateField.DD_MM_YYYY)

   # Custom format
   timestamp = DateField(
       name="Timestamp",
       format="%Y-%m-%d %H:%M:%S"
   )

**Predefined Formats:**

- ``DateField.MM_DD_YYYY``: "12/31/2023"
- ``DateField.DD_MM_YYYY``: "31/12/2023"

**Query Operators:**

Same as IntegerField (for date comparisons).

ListField
~~~~~~~~~

Maps delimited strings to Python lists.

.. code-block:: python

   from sheetalchemy import ListField

   # String items
   tags = ListField(
       name="Tags",
       delimiter=",",
       item_type=str
   )

   # Integer items
   scores = ListField(
       name="Scores",
       delimiter="|",
       item_type=int
   )

**Example Data:**

- Sheet: ``"python,django,web"``
- Python: ``["python", "django", "web"]``

CustomField
~~~~~~~~~~~

Define custom transformation logic.

.. code-block:: python

   from sheetalchemy import CustomField

   def calculate_bonus(data):
       base_salary = float(data.get("Base Salary", 0))
       performance = float(data.get("Performance", 0))
       return base_salary * performance * 0.1

   bonus = CustomField(to_value=calculate_bonus)

The ``to_value`` function receives the entire row data dictionary.

Field Parameters
----------------

Common Parameters
~~~~~~~~~~~~~~~~~

All fields support these parameters:

.. py:attribute:: name
   :type: str

   The exact column header name in Google Sheets (required).

.. py:attribute:: allow_empty_or_null
   :type: bool
   :value: True

   Whether to allow empty or null values.

.. py:attribute:: default_val
   :type: Any
   :value: None

   Default value if cell is empty.

.. py:attribute:: pre_transform
   :type: List[Callable]
   :value: []

   Functions to apply before type conversion.

.. py:attribute:: post_transform
   :type: List[Callable]
   :value: []

   Functions to apply after type conversion.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

   email = StringField(
       name="Email Address",
       allow_empty_or_null=False,
       default_val="",
       pre_transform=[str.lower, str.strip]
   )

Data Transformations
--------------------

Pre-Transformations
~~~~~~~~~~~~~~~~~~~

Applied to raw string data before type conversion:

.. code-block:: python

   from sheetalchemy import StringField
   from sheetalchemy.transformers import transform_to_lower_case

   name = StringField(
       name="Name",
       pre_transform=[transform_to_lower_case, str.strip]
   )

Post-Transformations
~~~~~~~~~~~~~~~~~~~~

Applied after type conversion:

.. code-block:: python

   def uppercase(value):
       return value.upper() if value else value

   code = StringField(
       name="Code",
       post_transform=[uppercase]
   )

Built-in Transformers
~~~~~~~~~~~~~~~~~~~~~

SheetAlchemy provides common transformers:

.. code-block:: python

   from sheetalchemy.transformers import (
       transform_to_lower_case,
       transform_to_upper_case,
       transform_strip_whitespace
   )

Field Validation
----------------

Validation happens automatically when data is loaded. Invalid data is tracked but doesn't prevent model instantiation.

Checking for Errors
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   user = Users.manager.get(name="John")
   
   # Get all validation errors
   errors = user.get_errors()
   if errors:
       print(f"Field errors: {errors}")
       # {'age': 'Invalid integer value', ...}

   # Get raw value that caused error
   raw_age = user.get_raw_value("age")
   print(f"Raw value: {raw_age}")

Common Validation Errors
~~~~~~~~~~~~~~~~~~~~~~~~

- **IntegerField**: Non-numeric values
- **DecimalField**: Non-numeric values
- **DateField**: Invalid date formats
- **BooleanField**: Rarely fails (defaults to False)

Custom Validation
~~~~~~~~~~~~~~~~~

Use CustomField for complex validation:

.. code-block:: python

   def validate_email(data):
       email = data.get("Email", "")
       if "@" not in email:
           raise ValueError(f"Invalid email: {email}")
       return email.lower()

   email = CustomField(to_value=validate_email)

Query Operators Reference
-------------------------

String Operators
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Operator
     - Usage
     - Description
   * - (none)
     - ``name="John"``
     - Exact match
   * - ``__ct``
     - ``name__ct="John"``
     - Contains substring

Numeric Operators
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Operator
     - Usage
     - Description
   * - (none)
     - ``age=25``
     - Equal to
   * - ``__lt``
     - ``age__lt=30``
     - Less than
   * - ``__lte``
     - ``age__lte=30``
     - Less than or equal
   * - ``__gt``
     - ``age__gt=18``
     - Greater than
   * - ``__gte``
     - ``age__gte=18``
     - Greater than or equal

Date Operators
~~~~~~~~~~~~~~

Same as numeric operators, applied to date values.

Boolean Operators
~~~~~~~~~~~~~~~~~

Only equality (``=``) is supported for BooleanField.

Best Practices
--------------

1. **Use Descriptive Field Names**

   .. code-block:: python

      first_name = StringField(name="First Name")  # Good
      fn = StringField(name="First Name")          # Bad

2. **Handle Optional Fields**

   .. code-block:: python

      middle_name = StringField(
          name="Middle Name",
          allow_empty_or_null=True,
          default_val=""
      )

3. **Choose Appropriate Field Types**

   .. code-block:: python

      # Good: Use IntegerField for whole numbers
      age = IntegerField(name="Age")
      
      # Bad: Using StringField for numbers
      age = StringField(name="Age")  # Loses numeric querying

4. **Use Transformers for Data Cleaning**

   .. code-block:: python

      email = StringField(
          name="Email",
          pre_transform=[str.lower, str.strip]
      )

5. **Document Custom Fields**

   .. code-block:: python

      def calculate_total(data):
          """Calculate total from quantity and price."""
          qty = int(data.get("Quantity", 0))
          price = float(data.get("Price", 0.0))
          return qty * price

      total = CustomField(to_value=calculate_total)

Common Patterns
---------------

Email Field
~~~~~~~~~~~

.. code-block:: python

   email = StringField(
       name="Email",
       allow_empty_or_null=False,
       pre_transform=[str.lower, str.strip]
   )

Percentage Field
~~~~~~~~~~~~~~~~

.. code-block:: python

   def parse_percentage(data):
       value = data.get("Completion", "0%")
       return float(value.replace("%", "")) / 100

   completion = CustomField(to_value=parse_percentage)

Multi-Select Field
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   categories = ListField(
       name="Categories",
       delimiter=",",
       item_type=str,
       pre_transform=[str.strip]
   )

Next Steps
----------

- :doc:`querying` - Learn how to query with fields
- :doc:`advanced` - Advanced field techniques
- :doc:`/api/fields` - Complete API reference
