# SheetAlchemy Tutorials

Welcome to the comprehensive SheetAlchemy tutorial series! These step-by-step guides will help you master Google Sheets ORM with Python.

## Tutorial Overview

### 🚀 [Getting Started](01_getting_started.md)
Learn the fundamentals of SheetAlchemy, from installation to creating your first models and performing basic operations.

**What you'll learn:**
- Installing SheetAlchemy and setting up Google Sheets API
- Creating your first model and fields
- Basic CRUD operations (Create, Read, Update, Delete)
- Authentication and sheet configuration
- Error handling basics

**Prerequisites:** Basic Python knowledge, Google account

**Estimated time:** 30 minutes

---

### 🎯 [Field Types](02_field_types.md)
Master all available field types and learn how to validate and transform your data.

**What you'll learn:**
- StringField, IntegerField, DecimalField, BooleanField, DateField
- ListField and CustomField for complex data
- Field validation and constraints
- Creating custom field types
- Best practices for field selection

**Prerequisites:** Completed Getting Started tutorial

**Estimated time:** 45 minutes

---

### 🔍 [Querying and Filtering](03_querying.md)
Explore SheetAlchemy's powerful Django-inspired querying API for data manipulation.

**What you'll learn:**
- Basic and advanced filtering techniques
- Lookup types (contains, startswith, gt, lt, etc.)
- Sorting and ordering data
- Complex queries with Q objects
- Pagination and performance optimization
- Aggregation and counting

**Prerequisites:** Completed Field Types tutorial

**Estimated time:** 60 minutes

---

### ⚡ [Advanced Usage](04_advanced_usage.md)
Dive into advanced patterns including custom managers, data transformers, and integration strategies.

**What you'll learn:**
- Custom managers for specialized queries
- Data transformers for automatic formatting
- Batch operations and performance optimization
- Model inheritance patterns
- Integration with Flask/Django
- Error handling and logging strategies
- Testing SheetAlchemy applications

**Prerequisites:** Completed all previous tutorials

**Estimated time:** 90 minutes

---

## Learning Path

### Beginner Path (2-3 hours)
1. **Getting Started** - Learn the basics
2. **Field Types** - Understand data modeling
3. Practice with the [Basic Example](../examples/basic_user_management.py)

### Intermediate Path (4-5 hours)
1. Complete Beginner Path
2. **Querying and Filtering** - Master data retrieval
3. Practice with the [Advanced Example](../examples/advanced_inventory_management.py)

### Advanced Path (6-8 hours)
1. Complete Intermediate Path
2. **Advanced Usage** - Learn expert patterns
3. Build your own application using SheetAlchemy
4. Contribute to the project

## Quick Reference

### Common Patterns

```python
# Model Definition
class Product(Model):
    name = StringField(required=True)
    price = IntegerField(min_value=0)
    category = StringField()
    is_active = BooleanField(default=True)
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Basic Operations
products = Product.objects
product = Product(name="Laptop", price=999)
product.save()

# Querying
all_products = products.all()
laptops = products.filter(name__contains="Laptop")
expensive = products.filter(price__gt=500).order_by('-price')

# Custom Manager
class ProductManager(Manager):
    def active(self):
        return self.filter(is_active=True)
    
    def by_category(self, category):
        return self.filter(category=category)

class Product(Model):
    # ... fields ...
    objects = ProductManager()
```

### Useful Code Snippets

```python
# Authentication
from sheetalchemy import authenticate
client = authenticate('service-account-key.json')

# Error Handling
from sheetalchemy.exceptions import ValidationError, SheetNotFoundError

try:
    product.save()
except ValidationError as e:
    print(f"Validation error: {e}")

# Environment Variables
import os
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# Batch Processing
def bulk_update(queryset, updates):
    for item in queryset:
        for key, value in updates.items():
            setattr(item, key, value)
        item.save()
```

## Troubleshooting Common Issues

### Authentication Problems
```python
# Check service account file path
import os
if not os.path.exists('path/to/service-account.json'):
    print("Service account file not found!")

# Verify sheet sharing
# Make sure your sheet is shared with the service account email
```

### Import Errors
```bash
# Install SheetAlchemy
pip install sheetalchemy

# Or install from source
pip install -e .
```

### Sheet Access Issues
```python
from sheetalchemy.exceptions import SheetNotFoundError

try:
    products = Product.objects.all()
except SheetNotFoundError:
    print("Sheet not found. Check sheet_id and permissions.")
```

## Additional Resources

### Examples
- [Basic User Management](../examples/basic_user_management.py) - Simple CRUD operations
- [Advanced Inventory Management](../examples/advanced_inventory_management.py) - Complex business logic

### Documentation
- [README](../README.md) - Project overview and installation
- [Contributing](../CONTRIBUTING.md) - How to contribute to SheetAlchemy
- [Privacy Policy](../PRIVACY.md) - Data handling and privacy

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Pull Requests**: Contribute code and improvements

## Tips for Success

1. **Start Small**: Begin with simple models and gradually add complexity
2. **Read Error Messages**: SheetAlchemy provides helpful error messages for debugging
3. **Use Type Hints**: Improve code quality with Python type annotations
4. **Test Early**: Write tests as you develop your models
5. **Follow Conventions**: Use consistent naming and structure
6. **Document Your Code**: Add docstrings and comments for maintainability

## What's Next?

After completing these tutorials, you'll be ready to:

- Build production SheetAlchemy applications
- Integrate SheetAlchemy with web frameworks
- Contribute to the SheetAlchemy project
- Help others in the community
- Explore advanced Google Sheets API features

Start with [Getting Started](01_getting_started.md) and begin your SheetAlchemy journey! 🎯