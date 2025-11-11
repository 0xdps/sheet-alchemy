# SheetAlchemy: Google Sheets Object-Relational Mapping (ORM)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/sheet-alchemy/badge/?version=latest)](https://sheet-alchemy.readthedocs.io/en/latest/?badge=latest)

SheetAlchemy is a Python library that provides an Object-Relational Mapping (ORM) interface for Google Sheets. It allows developers to interact with Google Sheets data using Python objects and Django-like query syntax, eliminating the need for repetitive Google Sheets API calls.

## 🚀 Features

- **Model-Based Approach**: Define Python classes that represent Google Sheets tabs
- **Rich Field Types**: Support for String, Integer, Date, Boolean, Decimal, List, and Custom fields
- **Django-Style Queries**: Familiar filtering and querying with field lookups (`__lt`, `__gt`, `__ct`, etc.)
- **Data Validation**: Built-in type validation and error handling
- **Load Policies**: Configure eager (`INIT`) or lazy (`LAZY`) data loading
- **Data Transformation**: Automatic cleaning of common spreadsheet issues (NA values, formula errors)
- **Authentication Management**: Seamless Google Sheets API authentication

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Field Types](#field-types)
- [Querying Data](#querying-data)
- [Advanced Usage](#advanced-usage)
- [Tutorials](#tutorials)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## 📦 Installation

### From GitHub (Current)

```sh
pip install git+https://github.com/0xdps/sheetalchemy.git
```

### From PyPI (Coming Soon)

```sh
pip install sheetalchemy
```

## 🚀 Quick Start

### 1. Setup Authentication

First, set up Google Sheets API authentication:

```python
from sheetalchemy import authenticate

# Option 1: Using service account key file
authenticate(key_path="/path/to/your/service-account-key.json")

# Option 2: Using environment variable
# Set SHEETALCHEMY_AUTH_KEY_PATH environment variable to your key file path
import os
os.environ['SHEETALCHEMY_AUTH_KEY_PATH'] = '/path/to/your/service-account-key.json'

# Option 3: Using key object directly
key_object = {
    "type": "service_account",
    "project_id": "your-project-id",
    # ... other key fields
}
authenticate(key_object=key_object)
```

### 2. Define Your Model

```python
from sheetalchemy import LoadPolicy, Model, StringField, IntegerField, DateField, BooleanField

class Users(Model):
    name = StringField(name="Name")
    age = IntegerField(name="Age")
    dob = DateField(name="DOB", format=DateField.MM_DD_YYYY, allow_empty=True, default_val="01/01/2010")
    is_family = BooleanField(name="Family")

    class Meta:
        sheet_name = "Test Sheet - SheetAlchemy"  # Google Sheet name
        tab_name = "Users"                # Worksheet/tab name
        header_index = 1                  # Row number containing headers (1-indexed)
        load_policy = LoadPolicy.LAZY     # Load data when first accessed
```

### 3. Query Your Data

```python
# Get all family members
family_users = Users.manager.filter(is_family=True)

# Get users under 30
young_users = Users.manager.filter(age__lt=30)

# Get a specific user
user = Users.manager.get(name="Devendra")

# Iterate through results
for family_member in family_users:
    print(f"Name: {family_member.name}, Age: {family_member.age}")
```

## 🔐 Authentication

SheetAlchemy uses Google Sheets API v4. You need to:

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account
4. Download the service account key JSON file
5. Share your Google Sheet with the service account email

For detailed authentication setup, see the [Google Sheets API documentation](https://developers.google.com/sheets/api/quickstart/python).

## 🏷️ Field Types

### StringField
```python
name = StringField(name="Name", allow_empty_or_null=True, default_val="Unknown")

# Query operators: eq (default), ct (contains)
Users.manager.filter(name="John")           # Exact match
Users.manager.filter(name__ct="John")       # Contains "John"
```

### IntegerField
```python
age = IntegerField(name="Age", allow_empty_or_null=False)

# Query operators: eq, lt, lte, gt, gte
Users.manager.filter(age=25)               # Equal to 25
Users.manager.filter(age__lt=30)           # Less than 30
Users.manager.filter(age__gte=18)          # Greater than or equal to 18
```

### DateField
```python
# Predefined formats
dob = DateField(name="DOB", format=DateField.MM_DD_YYYY)
created = DateField(name="Created", format=DateField.DD_MM_YYYY)

# Custom format
custom_date = DateField(name="CustomDate", format="%Y-%m-%d %H:%M:%S")
```

### BooleanField
```python
is_active = BooleanField(name="Active")

# Accepts: "true", "t", "yes", "y", "ok", "1" (case insensitive)
Users.manager.filter(is_active=True)
```

### DecimalField
```python
salary = DecimalField(name="Salary", allow_empty_or_null=True, default_val=0.0)

# Same operators as IntegerField
Users.manager.filter(salary__gt=50000.0)
```

### ListField
```python
# Comma-separated values converted to Python list
tags = ListField(name="Tags", delimiter=",", item_type=str)
scores = ListField(name="Scores", delimiter="|", item_type=int)
```

### CustomField
```python
# Define custom transformation logic
def calculate_bonus(data):
    base_salary = float(data.get("Base Salary", 0))
    return base_salary * 0.1

bonus = CustomField(to_value=calculate_bonus)
```

## 🔍 Querying Data

### Basic Queries

```python
# Get single record (raises exception if not found)
user = Users.manager.get(name="John")

# Filter records (returns iterator)
active_users = Users.manager.filter(is_active=True)
young_users = Users.manager.filter(age__lt=25)

# Multiple filters (AND operation)
young_family = Users.manager.filter(age__lt=30, is_family=True)
```

### Working with Results

```python
# Get iterator
results = Users.manager.filter(is_family=True)

# Iterate through results
for user in results:
    print(user.name, user.age)

# Access specific items
first_user = results.first()
last_user = results.last()
third_user = results.nth(2)

# Get count
total_count = results.size()

# Reset iterator
results.reset()
```

### Error Handling

```python
# Handle missing records
try:
    user = Users.manager.get(name="NonExistent")
except ModelItemException:
    print("User not found")

# Check for field errors
user = Users.manager.get(name="John")
errors = user.get_errors()
if errors:
    print(f"Field errors: {errors}")

# Access raw data
raw_data = user.get_raw_data()
raw_value = user.get_raw_value("name")
```

## 🔧 Advanced Usage

### Load Policies

```python
# LAZY: Load data when first accessed (default)
class LazyModel(GModel):
    class Meta:
        load_policy = LoadPolicy.LAZY

# INIT: Load data immediately when model is defined
class EagerModel(GModel):
    class Meta:
        load_policy = LoadPolicy.INIT
```

### Data Transformations

```python
from sheetalchemy.transformers import transform_to_lower_case

# Pre-processing transformations
name = StringField(
    name="Name", 
    pre_transform=[transform_to_lower_case]
)

# Post-processing transformations  
def uppercase_transform(value):
    return value.upper() if value else value

name = StringField(
    name="Name",
    post_transform=[uppercase_transform]
)
```

### Model Reloading

```python
# Reload model data from Google Sheets
Users.manager.reload_model()

# Initialize lazy-loaded model manually
Users.manager.initialise_model()
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Running tests
- Submitting pull requests
- Code style guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Privacy

Please review our [Privacy Policy](PRIVACY.md) for information about data handling and privacy considerations when using SheetAlchemy.

## 🆘 Support

- **Documentation**: [Read the Docs](https://sheet-alchemy.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/0xdps/sheet-alchemy/issues)
- **Tutorials**: [Getting Started Guide](tutorials/README.md)
- **Examples**: Complete applications in the [examples/](examples/) directory
- **Tests**: Comprehensive test suite in the [tests/](tests/) directory

## 📚 Requirements

- Python 3.8+
- gspread >= 6.0.0
- Google Sheets API access

## � Tutorials

Learn SheetAlchemy step by step with our comprehensive tutorial series:

- **[Getting Started](tutorials/01_getting_started.md)** - Installation, setup, and first models
- **[Field Types](tutorials/02_field_types.md)** - Complete guide to all field types and validation
- **[Querying & Filtering](tutorials/03_querying.md)** - Master data retrieval and filtering
- **[Advanced Usage](tutorials/04_advanced_usage.md)** - Custom managers, transformers, and optimization

📖 [**View All Tutorials**](tutorials/README.md)

## 💡 Examples

Explore complete example applications:

- **[Basic User Management](examples/basic_user_management.py)** - Simple CRUD operations and basic querying
- **[Advanced Inventory Management](examples/advanced_inventory_management.py)** - Complex business logic with multiple models

## �🗺️ Roadmap

- [x] ~~Add comprehensive unit tests~~
- [x] ~~Implement example applications~~
- [x] ~~Create detailed tutorials~~
- [ ] PyPI package publication
- [ ] More field types (JSONField, URLField)
- [ ] Bulk operations (create, update, delete)
- [ ] Query aggregation (sum, count, avg)
- [ ] Migration support for schema changes
- [ ] Better error reporting and debugging tools

## 🙏 Acknowledgments

- Built on top of the excellent [gspread](https://github.com/burnash/gspread) library
- Inspired by Django ORM patterns
- Thanks to all contributors and users

---

**Made with ❤️ by [Devendra Pratap Singh](https://github.com/0xdps)**
