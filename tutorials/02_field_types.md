# Field Types Tutorial

SheetAlchemy provides various field types to handle different data types in your Google Sheets. Each field type has specific validation rules and conversion methods.

## Core Field Types

### StringField

The most basic field type for text data.

```python
from sheetalchemy import Model, StringField

class Person(Model):
    # Basic string field
    name = StringField()
    
    # Required string field
    email = StringField(required=True)
    
    # String with maximum length
    bio = StringField(max_length=500)
    
    # String with default value
    status = StringField(default="active")

# Usage examples
person = Person(
    name="John Doe",
    email="john@example.com",
    bio="A software developer who loves Python",
    # status will default to "active"
)
```

**StringField Parameters:**
- `required` (bool): Field must have a value
- `default` (str): Default value if none provided
- `max_length` (int): Maximum character length
- `null` (bool): Allow None values

### IntegerField

For whole numbers.

```python
from sheetalchemy import Model, IntegerField

class Product(Model):
    name = StringField()
    
    # Basic integer
    quantity = IntegerField()
    
    # Integer with constraints
    price = IntegerField(min_value=0)  # Cannot be negative
    
    # Integer with range
    rating = IntegerField(min_value=1, max_value=5)
    
    # Integer with default
    views = IntegerField(default=0)

# Usage examples
product = Product(
    name="Laptop",
    quantity=10,
    price=999,
    rating=4
    # views defaults to 0
)

# Validation happens on save
try:
    bad_product = Product(name="Test", rating=10)  # rating > 5
    bad_product.save()  # Will raise ValidationError
except ValidationError as e:
    print(f"Validation error: {e}")
```

**IntegerField Parameters:**
- `min_value` (int): Minimum allowed value
- `max_value` (int): Maximum allowed value
- `required` (bool): Field must have a value
- `default` (int): Default value if none provided

### DecimalField

For precise decimal numbers and currency.

```python
from sheetalchemy import Model, DecimalField
from decimal import Decimal

class Invoice(Model):
    invoice_number = StringField()
    
    # Basic decimal field
    amount = DecimalField()
    
    # Decimal with precision control
    tax_rate = DecimalField(max_digits=5, decimal_places=4)  # e.g., 0.0825
    
    # Currency field
    total = DecimalField(max_digits=10, decimal_places=2)  # e.g., 1234.56

# Usage examples
invoice = Invoice(
    invoice_number="INV-001",
    amount=Decimal('100.00'),
    tax_rate=Decimal('0.0825'),
    total=Decimal('108.25')
)

# Can also use strings or floats (converted to Decimal)
invoice2 = Invoice(
    invoice_number="INV-002",
    amount="250.50",
    tax_rate=0.08,
    total=270.54
)
```

**DecimalField Parameters:**
- `max_digits` (int): Total number of digits
- `decimal_places` (int): Number of decimal places
- `min_value` (Decimal): Minimum allowed value
- `max_value` (Decimal): Maximum allowed value

### BooleanField

For True/False values.

```python
from sheetalchemy import Model, BooleanField

class User(Model):
    username = StringField()
    
    # Basic boolean
    is_active = BooleanField()
    
    # Boolean with default
    is_verified = BooleanField(default=False)
    
    # Boolean that allows None
    newsletter_opt_in = BooleanField(null=True)

# Usage examples
user = User(
    username="johndoe",
    is_active=True,
    # is_verified defaults to False
    newsletter_opt_in=None  # User hasn't decided yet
)

# Google Sheets representation
# True -> "TRUE", False -> "FALSE", None -> ""
```

**BooleanField Parameters:**
- `default` (bool): Default value if none provided
- `null` (bool): Allow None values

### DateField

For date values (without time).

```python
from sheetalchemy import Model, DateField
from datetime import date, datetime

class Event(Model):
    title = StringField()
    
    # Basic date field
    event_date = DateField()
    
    # Date with default (today)
    created_date = DateField(default=date.today)
    
    # Date that can be null
    cancelled_date = DateField(null=True)

# Usage examples
event = Event(
    title="Annual Conference",
    event_date=date(2024, 6, 15),
    # created_date will be set to today
    cancelled_date=None
)

# Alternative ways to set dates
event2 = Event(
    title="Workshop",
    event_date="2024-07-20",  # String format
    created_date=datetime.now().date()  # From datetime
)
```

**DateField Parameters:**
- `default` (callable or date): Default value if none provided
- `null` (bool): Allow None values
- `auto_now` (bool): Automatically set to current date on save
- `auto_now_add` (bool): Set to current date on creation only

### ListField

For storing lists of values (stored as JSON in sheets).

```python
from sheetalchemy import Model, ListField

class Article(Model):
    title = StringField()
    
    # List of strings
    tags = ListField()
    
    # List with specific item type validation
    categories = ListField(item_type=str)
    
    # List with maximum items
    keywords = ListField(max_items=10)

# Usage examples
article = Article(
    title="Python Tutorial",
    tags=["python", "tutorial", "programming"],
    categories=["education", "technology"],
    keywords=["python", "beginner", "coding"]
)

# After saving to sheets, lists are stored as JSON strings
# In Google Sheets: '["python", "tutorial", "programming"]'
```

**ListField Parameters:**
- `item_type` (type): Type validation for list items
- `max_items` (int): Maximum number of items allowed
- `min_items` (int): Minimum number of items required

### CustomField

For custom data types and transformations.

```python
from sheetalchemy import Model, CustomField
import json

class JSONField(CustomField):
    """Custom field that stores Python objects as JSON."""
    
    def to_sheet_value(self, value):
        """Convert Python value to sheet string."""
        if value is None:
            return ""
        return json.dumps(value)
    
    def from_sheet_value(self, value):
        """Convert sheet string back to Python value."""
        if not value:
            return None
        return json.loads(value)

class Configuration(Model):
    name = StringField()
    
    # Use custom JSON field
    settings = JSONField()
    
    # Another custom field example
    metadata = JSONField()

# Usage examples
config = Configuration(
    name="App Config",
    settings={
        "theme": "dark",
        "language": "en",
        "notifications": True
    },
    metadata={"version": "1.0", "author": "John Doe"}
)

# Values are automatically serialized/deserialized
config.save()
loaded_config = Configuration.objects.filter(name="App Config").first()
print(loaded_config.settings["theme"])  # "dark"
```

## Advanced Field Examples

### Email Validation Field

```python
import re
from sheetalchemy import CustomField
from sheetalchemy.exceptions import ValidationError

class EmailField(CustomField):
    """Custom field with email validation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_regex = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
    
    def validate(self, value):
        super().validate(value)
        if value and not self.email_regex.match(value):
            raise ValidationError(f"Invalid email format: {value}")
    
    def to_sheet_value(self, value):
        return value or ""
    
    def from_sheet_value(self, value):
        return value if value else None

class Contact(Model):
    name = StringField()
    email = EmailField(required=True)
```

### URL Field

```python
from urllib.parse import urlparse

class URLField(CustomField):
    """Field that validates and normalizes URLs."""
    
    def validate(self, value):
        super().validate(value)
        if value:
            try:
                result = urlparse(value)
                if not all([result.scheme, result.netloc]):
                    raise ValueError("Invalid URL")
            except ValueError:
                raise ValidationError(f"Invalid URL: {value}")
    
    def to_sheet_value(self, value):
        if not value:
            return ""
        # Ensure URL has scheme
        if not value.startswith(('http://', 'https://')):
            return f"https://{value}"
        return value

class Website(Model):
    name = StringField()
    url = URLField()
    description = StringField()
```

### Enum Field

```python
from enum import Enum

class StatusEnum(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class EnumField(CustomField):
    """Field that accepts only enum values."""
    
    def __init__(self, enum_class, **kwargs):
        super().__init__(**kwargs)
        self.enum_class = enum_class
    
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if isinstance(value, str):
                # Try to convert string to enum
                try:
                    value = self.enum_class(value)
                except ValueError:
                    raise ValidationError(f"Invalid choice: {value}")
            elif not isinstance(value, self.enum_class):
                raise ValidationError(f"Must be {self.enum_class.__name__} instance")
    
    def to_sheet_value(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        return value or ""
    
    def from_sheet_value(self, value):
        if value:
            return self.enum_class(value)
        return None

class BlogPost(Model):
    title = StringField()
    content = StringField()
    status = EnumField(StatusEnum, default=StatusEnum.DRAFT)
```

## Field Options Reference

### Common Parameters

All field types support these common parameters:

```python
field = SomeField(
    required=True,          # Field must have a value
    default=some_value,     # Default value (can be callable)
    null=False,            # Allow None values
    blank=False,           # Allow empty strings (StringField only)
    validators=[func1, func2],  # Custom validation functions
    help_text="Description"     # Documentation
)
```

### Validation Functions

You can add custom validators to any field:

```python
def validate_positive(value):
    if value <= 0:
        raise ValidationError("Value must be positive")

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError("Value must be even")

class Number(Model):
    value = IntegerField(validators=[validate_positive, validate_even])
```

## Working with Field Values

### Getting and Setting Values

```python
# Create a model instance
user = User(name="John", age=25)

# Get field values
print(user.name)  # "John"
print(user.age)   # 25

# Set field values
user.name = "Jane"
user.age = 30

# Check if field has value
if user.email:
    print(f"Email: {user.email}")

# Get field with default
status = user.status or "inactive"
```

### Field Metadata

```python
# Access field information
name_field = User._meta.get_field('name')
print(name_field.required)  # True/False
print(name_field.default)   # Default value
print(name_field.__class__.__name__)  # "StringField"

# List all fields
for field_name, field in User._meta.fields.items():
    print(f"{field_name}: {field.__class__.__name__}")
```

## Best Practices

### 1. Choose the Right Field Type

```python
# Good: Use appropriate types
class Order(Model):
    order_id = StringField()        # Text identifier
    quantity = IntegerField()       # Whole numbers
    price = DecimalField()         # Precise currency
    is_paid = BooleanField()       # True/False status
    order_date = DateField()       # Date values

# Avoid: Using strings for everything
class BadOrder(Model):
    order_id = StringField()
    quantity = StringField()       # Should be IntegerField
    price = StringField()          # Should be DecimalField
    is_paid = StringField()        # Should be BooleanField
```

### 2. Use Validation

```python
# Good: Add appropriate validation
class Product(Model):
    name = StringField(required=True, max_length=100)
    price = DecimalField(min_value=0, max_digits=10, decimal_places=2)
    rating = IntegerField(min_value=1, max_value=5)

# Consider: Custom validation for complex rules
def validate_sku(value):
    if not value.startswith('SKU-'):
        raise ValidationError("SKU must start with 'SKU-'")

class Product(Model):
    sku = StringField(validators=[validate_sku])
```

### 3. Provide Sensible Defaults

```python
class User(Model):
    username = StringField(required=True)
    is_active = BooleanField(default=True)    # Most users are active
    created_date = DateField(default=date.today)
    login_count = IntegerField(default=0)
```

### 4. Document Your Fields

```python
class Employee(Model):
    employee_id = StringField(
        required=True,
        help_text="Unique employee identifier (e.g., EMP001)"
    )
    salary = DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Annual salary in USD"
    )
    department = StringField(
        help_text="Department name (Engineering, Sales, etc.)"
    )
```

## Next Steps

Now that you understand field types:

1. **Learn advanced querying**: Check out the [Querying Tutorial](03_querying.md)
2. **Explore model relationships**: See the [Advanced Usage Tutorial](04_advanced_usage.md)
3. **Try field examples**: Look at the complete examples in the `examples/` directory

## Common Field Patterns Cheat Sheet

```python
# User/Account fields
email = EmailField(required=True)
password_hash = StringField(required=True)
is_active = BooleanField(default=True)
created_at = DateField(default=date.today)
last_login = DateField(null=True)

# Product/Inventory fields
name = StringField(required=True, max_length=200)
description = StringField(max_length=1000)
price = DecimalField(max_digits=10, decimal_places=2, min_value=0)
quantity = IntegerField(min_value=0)
is_available = BooleanField(default=True)

# Content/Blog fields
title = StringField(required=True, max_length=200)
content = StringField()
tags = ListField()
published_date = DateField(null=True)
is_published = BooleanField(default=False)
view_count = IntegerField(default=0)

# Settings/Configuration fields
config_key = StringField(required=True)
config_value = JSONField()
is_enabled = BooleanField(default=True)
updated_at = DateField(auto_now=True)
```