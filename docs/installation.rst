Installation
============

Requirements
------------

SheetAlchemy requires:

- Python 3.8 or higher
- gspread >= 6.2.0
- Google Sheets API access

Installing SheetAlchemy
-----------------------

From PyPI
~~~~~~~~~

The recommended way to install SheetAlchemy is via pip:

.. code-block:: bash

   pip install sheetalchemy

From GitHub
~~~~~~~~~~~

To install the latest development version:

.. code-block:: bash

   pip install git+https://github.com/0xdps/sheet-alchemy.git

For Development
~~~~~~~~~~~~~~~

If you want to contribute to SheetAlchemy, clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/0xdps/sheet-alchemy.git
   cd sheet-alchemy
   pip install -e ".[dev]"

This will install SheetAlchemy along with all development dependencies including:

- pytest (testing)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

Installing Dependencies
-----------------------

Core Dependencies
~~~~~~~~~~~~~~~~~

SheetAlchemy has minimal core dependencies:

.. code-block:: bash

   pip install gspread>=6.2.0

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

For development and testing:

.. code-block:: bash

   pip install sheetalchemy[dev]

Verifying Installation
----------------------

To verify that SheetAlchemy is installed correctly:

.. code-block:: python

   import sheetalchemy
   print(sheetalchemy.__version__)

You should see the version number printed (e.g., ``2.0``).

Google Sheets API Setup
-----------------------

Before using SheetAlchemy, you need to set up Google Sheets API access:

1. **Create a Google Cloud Project**

   - Go to the `Google Cloud Console <https://console.cloud.google.com/>`_
   - Create a new project or select an existing one

2. **Enable Google Sheets API**

   - In your project, go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create Service Account**

   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"

4. **Generate Key**

   - Click on the created service account
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Save the downloaded key file securely

5. **Share Your Google Sheet**

   - Open your Google Sheet
   - Click "Share"
   - Add the service account email (found in the JSON key file)
   - Give it "Editor" access

Next Steps
----------

Once installed, proceed to the :doc:`quickstart` guide to learn how to use SheetAlchemy.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ModuleNotFoundError: No module named 'gspread'**

Make sure gspread is installed:

.. code-block:: bash

   pip install gspread>=6.2.0

**Authentication Errors**

Ensure your service account has access to the Google Sheet and the API is enabled in your Google Cloud Project.

**Version Conflicts**

If you encounter dependency conflicts, try creating a fresh virtual environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install sheetalchemy
