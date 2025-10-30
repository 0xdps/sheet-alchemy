# Getting Started with SheetAlchemy

SheetAlchemy (Google Sheets Object-Relational Mapping) is a Python library that provides an ORM-like interface for Google Sheets, allowing you to work with spreadsheet data using familiar Python patterns.

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher
- A Google Cloud Project with Sheets API enabled
- Service account credentials (JSON file)

## Installation

### Using pip

```bash
pip install sheetalchemy
```

### From source

```bash
git clone https://github.com/0xdps/sheetalchemy.git
cd sheetalchemy
pip install -e .
```

## Setting up Google Sheets API

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API

### 2. Create Service Account Credentials

1. Navigate to "Credentials" in the Google Cloud Console
2. Click "Create Credentials" → "Service Account"
3. Fill in the service account details
4. Download the JSON key file
5. Store it securely (never commit to version control!)

### 3. Share Your Google Sheet

1. Create a new Google Sheet
2. Share it with your service account email address
3. Give the service account "Editor" permissions

## Your First SheetAlchemy Model

Let's create a simple model to manage user data in a Google Sheet.

### Step 1: Set up Authentication

Create a file called `auth_config.py`:

```python
from sheetalchemy import authenticate

# Replace with your service account file path
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-key.json'

# Authenticate once, use everywhere
client = authenticate(SERVICE_ACCOUNT_FILE)
```

### Step 2: Define Your Model

Create a file called `models.py`:

```python
from sheetalchemy import Model, StringField, IntegerField, DateField
from auth_config import client

class User(Model):
    """A simple user model for demonstration."""
    
    # Define fields that correspond to columns in your sheet
    name = StringField(required=True)
    email = StringField(required=True)
    age = IntegerField()
    join_date = DateField()
    
    class Meta:
        # Replace with your Google Sheet ID
        sheet_id = 'your-google-sheet-id-here'
        worksheet_name = 'Users'  # Name of the worksheet/tab
        client = client

# The model automatically creates the manager
users = User.objects
```

### Step 3: Create Your First Records

```python
from models import User
from datetime import date

# Create a new user
new_user = User(
    name="John Doe",
    email="john@example.com", 
    age=25,
    join_date=date.today()
)

# Save to Google Sheets
new_user.save()
print(f"Created user: {new_user.name}")

# Create multiple users at once
users_data = [
    {"name": "Alice Smith", "email": "alice@example.com", "age": 30},
    {"name": "Bob Johnson", "email": "bob@example.com", "age": 28},
    {"name": "Carol Wilson", "email": "carol@example.com", "age": 32}
]

for user_data in users_data:
    user = User(**user_data)
    user.save()
    print(f"Created user: {user.name}")
```

### Step 4: Query Your Data

```python
from models import users

# Get all users
all_users = users.all()
print(f"Total users: {len(all_users)}")

# Filter users
young_users = users.filter(age__lt=30)
print(f"Users under 30: {[u.name for u in young_users]}")

# Get a specific user
john = users.filter(name="John Doe").first()
if john:
    print(f"Found John: {john.email}")

# Get users by email domain
gmail_users = users.filter(email__contains="@gmail.com")
print(f"Gmail users: {len(gmail_users)}")
```

### Step 5: Update Records

```python
# Update a single user
john = users.filter(name="John Doe").first()
if john:
    john.age = 26
    john.save()
    print(f"Updated {john.name}'s age to {john.age}")

# Update multiple users
for user in users.filter(age__gt=30):
    user.age += 1  # Happy birthday!
    user.save()
```

### Step 6: Delete Records

```python
# Delete a specific user
user_to_delete = users.filter(email="john@example.com").first()
if user_to_delete:
    user_to_delete.delete()
    print(f"Deleted user: {user_to_delete.name}")

# Delete multiple users (be careful!)
inactive_users = users.filter(age__gt=50)
for user in inactive_users:
    user.delete()
```

## Complete Example

Here's a complete working example you can run:

```python
# complete_example.py
from sheetalchemy import Model, StringField, IntegerField, authenticate
from datetime import date

# 1. Authenticate
client = authenticate('path/to/your/service-account-key.json')

# 2. Define Model
class Contact(Model):
    name = StringField(required=True)
    phone = StringField()
    age = IntegerField()
    
    class Meta:
        sheet_id = 'your-google-sheet-id'
        worksheet_name = 'Contacts'
        client = client

# 3. Use the model
if __name__ == "__main__":
    contacts = Contact.objects
    
    # Create some contacts
    contact1 = Contact(name="Jane Doe", phone="555-0123", age=29)
    contact1.save()
    
    contact2 = Contact(name="Mike Wilson", phone="555-0456", age=35)
    contact2.save()
    
    # Query contacts
    all_contacts = contacts.all()
    print(f"All contacts: {[c.name for c in all_contacts]}")
    
    # Filter contacts
    young_contacts = contacts.filter(age__lt=30)
    print(f"Young contacts: {[c.name for c in young_contacts]}")
    
    # Update a contact
    jane = contacts.filter(name="Jane Doe").first()
    if jane:
        jane.age = 30
        jane.save()
        print(f"Updated Jane's age to {jane.age}")
```

## Understanding the Google Sheet Structure

When you run your SheetAlchemy code, it will automatically:

1. **Create headers**: The first row will contain field names
2. **Add data rows**: Each model instance becomes a row
3. **Handle types**: Automatically convert Python types to sheet values

Your sheet will look like this:

| name | phone | age |
|------|-------|-----|
| Jane Doe | 555-0123 | 30 |
| Mike Wilson | 555-0456 | 35 |

## Common Patterns

### Error Handling

```python
from sheetalchemy.exceptions import ValidationError, SheetNotFoundError

try:
    user = User(name="", email="invalid-email")  # Invalid data
    user.save()
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    users = User.objects.all()
except SheetNotFoundError as e:
    print(f"Sheet not found: {e}")
```

### Working with Dates

```python
from datetime import date, datetime
from sheetalchemy import DateField

class Event(Model):
    title = StringField()
    event_date = DateField()
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Create events
event = Event(
    title="Meeting",
    event_date=date(2024, 1, 15)
)
event.save()

# Filter by date
recent_events = Event.objects.filter(event_date__gte=date.today())
```

### Environment Variables for Security

Create a `.env` file:

```bash
GOOGLE_SHEET_ID=your-google-sheet-id-here
SERVICE_ACCOUNT_FILE=path/to/service-account.json
```

Use in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
```

## Next Steps

Now that you understand the basics:

1. **Learn about field types**: Read the [Field Types Tutorial](02_field_types.md)
2. **Master querying**: Check out the [Querying Tutorial](03_querying.md)
3. **Explore advanced features**: See the [Advanced Usage Tutorial](04_advanced_usage.md)
4. **Try the examples**: Look at the complete examples in the `examples/` directory

## Troubleshooting

### Common Issues

**Authentication Error**: Make sure your service account JSON file path is correct and the file exists.

**Permission Denied**: Ensure you've shared your Google Sheet with the service account email address.

**Sheet Not Found**: Verify your `sheet_id` is correct and the worksheet name matches exactly.

**Import Error**: Make sure SheetAlchemy is installed: `pip install sheetalchemy`

### Getting Help

- Check the [FAQ](../README.md#faq)
- Look at [example applications](../examples/)
- Open an issue on GitHub

Happy coding with SheetAlchemy! 🚀