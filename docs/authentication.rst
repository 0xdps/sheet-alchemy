Authentication
==============

SheetAlchemy uses Google Sheets API v4 for accessing your spreadsheet data. This guide covers all authentication methods and best practices.

Overview
--------

To use SheetAlchemy, you need:

1. A Google Cloud Project with Google Sheets API enabled
2. A Service Account with credentials
3. The service account must have access to your Google Sheets

Authentication Methods
----------------------

SheetAlchemy supports three authentication methods:

1. Key File Path
2. Key Object
3. Environment Variable

Method 1: Key File Path
~~~~~~~~~~~~~~~~~~~~~~~~

The most common method is using a service account key file:

.. code-block:: python

   from sheetalchemy import authenticate

   authenticate(key_path="/path/to/service-account-key.json")

This is recommended for:

- Development environments
- Local testing
- Simple deployments

Method 2: Key Object
~~~~~~~~~~~~~~~~~~~~

Pass the service account key as a Python dictionary:

.. code-block:: python

   from sheetalchemy import authenticate

   key_object = {
       "type": "service_account",
       "project_id": "your-project-id",
       "private_key_id": "key-id",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
       "client_email": "your-service-account@project.iam.gserviceaccount.com",
       "client_id": "123456789",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
       "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
   }

   authenticate(key_object=key_object)

This is useful for:

- Production environments
- Cloud deployments (AWS, GCP, Azure)
- When credentials are stored in secret managers

Method 3: Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the ``SHEETALCHEMY_AUTH_KEY_PATH`` environment variable:

.. code-block:: bash

   export SHEETALCHEMY_AUTH_KEY_PATH="/path/to/service-account-key.json"

Then authenticate without parameters:

.. code-block:: python

   from sheetalchemy import authenticate
   
   # Will automatically use SHEETALCHEMY_AUTH_KEY_PATH
   authenticate()

Or set it in Python:

.. code-block:: python

   import os
   os.environ['SHEETALCHEMY_AUTH_KEY_PATH'] = '/path/to/key.json'

This is recommended for:

- CI/CD pipelines
- Containerized applications
- 12-factor app compliance

Setting Up Google Sheets API
-----------------------------

Step-by-Step Guide
~~~~~~~~~~~~~~~~~~

1. **Create Google Cloud Project**

   - Go to `Google Cloud Console <https://console.cloud.google.com/>`_
   - Click "Select a project" → "New Project"
   - Name your project and click "Create"

2. **Enable Google Sheets API**

   - In the project dashboard, go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"

3. **Create Service Account**

   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in:
     
     - Service account name: e.g., "sheetalchemy-service"
     - Service account ID: auto-generated
     - Description: "Service account for SheetAlchemy"
   
   - Click "Create and Continue"
   - Skip optional steps and click "Done"

4. **Create and Download Key**

   - Click on the created service account
   - Go to the "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON" format
   - The key file will download automatically
   - **Store this file securely** - it contains sensitive credentials

5. **Share Google Sheet with Service Account**

   - Open your Google Sheet
   - Click the "Share" button
   - Copy the service account email from the JSON key file
     (looks like: ``sheetalchemy-service@your-project.iam.gserviceaccount.com``)
   - Paste it in the share dialog
   - Give it "Editor" permission
   - Uncheck "Notify people"
   - Click "Share"

Security Best Practices
-----------------------

Protecting Credentials
~~~~~~~~~~~~~~~~~~~~~~

**DO:**

- Store key files outside your project directory
- Use environment variables for key paths
- Add key files to ``.gitignore``
- Use secret managers in production (AWS Secrets Manager, GCP Secret Manager, etc.)
- Restrict service account permissions to only required sheets

**DON'T:**

- Commit key files to version control
- Share key files via email or chat
- Use the same service account across multiple projects
- Give service accounts more permissions than needed

Example .gitignore Entry
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   # Google Sheets API credentials
   *service-account*.json
   credentials.json
   .env

Using Secret Managers
~~~~~~~~~~~~~~~~~~~~~

AWS Secrets Manager Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import boto3
   import json
   from sheetalchemy import authenticate

   def get_secret():
       session = boto3.session.Session()
       client = session.client(
           service_name='secretsmanager',
           region_name='us-east-1'
       )
       
       secret = client.get_secret_value(SecretId='sheetalchemy/credentials')
       return json.loads(secret['SecretString'])

   # Authenticate with secret
   key_object = get_secret()
   authenticate(key_object=key_object)

Environment-Specific Configuration
-----------------------------------

Development
~~~~~~~~~~~

.. code-block:: python

   # config/dev.py
   from sheetalchemy import authenticate

   authenticate(key_path="dev-credentials.json")

Production
~~~~~~~~~~

.. code-block:: python

   # config/prod.py
   import os
   from sheetalchemy import authenticate

   # Use environment variable
   authenticate(key_path=os.getenv('GOOGLE_SHEETS_KEY_PATH'))

Using .env Files
~~~~~~~~~~~~~~~~

For development, use python-dotenv:

.. code-block:: bash

   pip install python-dotenv

.. code-block:: python

   # .env file
   SHEETALCHEMY_AUTH_KEY_PATH=/path/to/service-account-key.json

.. code-block:: python

   # app.py
   from dotenv import load_dotenv
   from sheetalchemy import authenticate

   load_dotenv()
   authenticate()  # Automatically uses env variable

Troubleshooting
---------------

Common Authentication Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error: "File not found"**

.. code-block:: python

   # Check if file exists
   import os
   key_path = "/path/to/key.json"
   if not os.path.exists(key_path):
       print(f"Key file not found at: {key_path}")

**Error: "Insufficient Permission"**

- Make sure the service account email is added to your Google Sheet with Editor access
- Verify the Google Sheets API is enabled in your Google Cloud Project

**Error: "Invalid credentials"**

- Ensure the JSON key file is valid and not corrupted
- Try downloading a new key file from Google Cloud Console

**Error: "API has not been enabled"**

- Go to Google Cloud Console → APIs & Services → Library
- Enable "Google Sheets API"

Checking Authentication Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sheetalchemy._auth import get_sheet

   try:
       # Try to access a sheet
       sheet = get_sheet("Your Sheet Name", "Your Tab")
       print("Authentication successful!")
   except Exception as e:
       print(f"Authentication failed: {e}")

Advanced: Multiple Service Accounts
------------------------------------

If you need to access different sheets with different credentials:

.. code-block:: python

   from sheetalchemy import authenticate

   # Authenticate for different sheets
   def setup_auth_for_sheet(sheet_name):
       if sheet_name == "Company Data":
           authenticate(key_path="company-credentials.json")
       elif sheet_name == "Personal Data":
           authenticate(key_path="personal-credentials.json")

   setup_auth_for_sheet("Company Data")

Note: SheetAlchemy uses a global authentication state, so re-authenticating will override the previous authentication.

Next Steps
----------

Now that you've set up authentication, learn about:

- :doc:`models` - Define your data models
- :doc:`fields` - Available field types
- :doc:`quickstart` - Complete quick start guide
