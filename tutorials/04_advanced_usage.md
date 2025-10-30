# Advanced Usage Tutorial

This tutorial covers advanced SheetAlchemy features including custom managers, data transformers, batch operations, performance optimization, and integration patterns.

## Custom Managers

Managers provide a way to add custom query methods and encapsulate common database operations.

### Creating Custom Managers

```python
from sheetalchemy import Manager, Model, StringField, IntegerField, BooleanField, DateField
from datetime import date, timedelta

class ProductManager(Manager):
    """Custom manager for Product model with specialized queries."""
    
    def active(self):
        """Get only active products."""
        return self.filter(is_active=True)
    
    def by_category(self, category):
        """Get products by category."""
        return self.filter(category__iexact=category)
    
    def expensive(self, threshold=1000):
        """Get products above price threshold."""
        return self.filter(price__gt=threshold)
    
    def featured(self):
        """Get featured products."""
        return self.filter(is_featured=True, is_active=True).order_by('-created_date')
    
    def search(self, query):
        """Search products by name or description."""
        from sheetalchemy import Q
        return self.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    def low_stock(self, threshold=5):
        """Get products with low stock."""
        return self.filter(stock__lte=threshold, is_active=True)

class Product(Model):
    name = StringField(required=True)
    description = StringField()
    price = IntegerField()
    stock = IntegerField(default=0)
    category = StringField()
    is_active = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    created_date = DateField(default=date.today)
    
    # Use custom manager
    objects = ProductManager()
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Usage examples
active_products = Product.objects.active()
electronics = Product.objects.by_category('Electronics')
expensive_items = Product.objects.expensive(500)
featured_products = Product.objects.featured()
search_results = Product.objects.search('laptop')
low_stock_items = Product.objects.low_stock(3)
```

### Chaining Manager Methods

```python
# Chain custom methods with built-in filters
expensive_electronics = (
    Product.objects
    .active()
    .by_category('Electronics')
    .expensive(800)
    .order_by('-price')
)

# Complex search with multiple filters
premium_search = (
    Product.objects
    .search('gaming')
    .expensive(1000)
    .featured()
    [:5]
)
```

### Multiple Managers

```python
class AllProductsManager(Manager):
    """Manager that includes inactive products."""
    pass

class ActiveProductsManager(Manager):
    """Manager for only active products."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Product(Model):
    name = StringField()
    is_active = BooleanField(default=True)
    
    # Multiple managers
    all_objects = AllProductsManager()  # All products
    objects = ActiveProductsManager()   # Only active (default)
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Usage
all_products = Product.all_objects.all()      # Includes inactive
active_products = Product.objects.all()       # Only active
```

## Data Transformers

Transformers allow you to modify data before saving to sheets and after loading from sheets.

### Built-in Transformers

```python
from sheetalchemy.transformers import UpperCaseTransformer, LowerCaseTransformer, SlugTransformer

class Article(Model):
    title = StringField()
    slug = StringField(transformer=SlugTransformer())        # "My Article" -> "my-article"
    author = StringField(transformer=UpperCaseTransformer()) # "john doe" -> "JOHN DOE"
    tags = StringField(transformer=LowerCaseTransformer())   # "Python, WEB" -> "python, web"
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Usage
article = Article(
    title="My First Article",
    slug="My First Article",  # Will become "my-first-article"
    author="john doe",        # Will become "JOHN DOE"
    tags="Python, WEB"       # Will become "python, web"
)
article.save()
```

### Custom Transformers

```python
from sheetalchemy.transformers import BaseTransformer
import re

class PhoneNumberTransformer(BaseTransformer):
    """Transform phone numbers to a standard format."""
    
    def to_sheet(self, value):
        """Format phone number for storage."""
        if not value:
            return ""
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', value)
        
        # Format as (XXX) XXX-XXXX
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return value  # Invalid format, return as-is
    
    def from_sheet(self, value):
        """Load formatted phone number."""
        return value  # Already formatted

class PriceTransformer(BaseTransformer):
    """Transform prices to include currency symbol."""
    
    def to_sheet(self, value):
        """Store price with currency."""
        if value is None:
            return ""
        return f"${value:.2f}"
    
    def from_sheet(self, value):
        """Parse price from sheet."""
        if not value:
            return None
        # Remove $ and convert to float
        return float(value.replace('$', '').replace(',', ''))

class Contact(Model):
    name = StringField()
    phone = StringField(transformer=PhoneNumberTransformer())
    
class Product(Model):
    name = StringField()
    price = IntegerField(transformer=PriceTransformer())
```

### JSON Transformer

```python
import json
from sheetalchemy.transformers import BaseTransformer

class JSONTransformer(BaseTransformer):
    """Store Python objects as JSON strings."""
    
    def to_sheet(self, value):
        if value is None:
            return ""
        return json.dumps(value, ensure_ascii=False)
    
    def from_sheet(self, value):
        if not value:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value  # Return raw value if not valid JSON

class Configuration(Model):
    name = StringField()
    settings = StringField(transformer=JSONTransformer())
    metadata = StringField(transformer=JSONTransformer())

# Usage
config = Configuration(
    name="App Settings",
    settings={
        "theme": "dark",
        "language": "en",
        "notifications": True
    },
    metadata={"version": "1.0", "author": "John Doe"}
)
config.save()

# When loaded, settings and metadata are automatically converted back to dict
loaded_config = Configuration.objects.filter(name="App Settings").first()
print(loaded_config.settings["theme"])  # "dark"
```

## Batch Operations

Optimize performance when working with large datasets.

### Bulk Create

```python
def bulk_create_products(product_data):
    """Create multiple products efficiently."""
    products = []
    
    for data in product_data:
        product = Product(
            name=data['name'],
            price=data['price'],
            category=data['category']
        )
        products.append(product)
    
    # Save all at once (more efficient than individual saves)
    for product in products:
        product.save()
    
    return products

# Usage
product_data = [
    {"name": "Laptop A", "price": 999, "category": "Electronics"},
    {"name": "Laptop B", "price": 1299, "category": "Electronics"},
    {"name": "Mouse", "price": 25, "category": "Electronics"},
]
created_products = bulk_create_products(product_data)
```

### Bulk Update

```python
def bulk_update_prices(category, increase_percent):
    """Update prices for all products in a category."""
    products = Product.objects.filter(category=category)
    
    updated_count = 0
    for product in products:
        old_price = product.price
        product.price = int(old_price * (1 + increase_percent / 100))
        product.save()
        updated_count += 1
        
        if updated_count % 10 == 0:
            print(f"Updated {updated_count} products...")
    
    return updated_count

# Usage
updated = bulk_update_prices("Electronics", 5.0)  # 5% increase
print(f"Updated {updated} electronics prices")
```

### Batch Processing with Progress

```python
def process_large_dataset(batch_size=100):
    """Process large datasets in batches with progress tracking."""
    all_products = Product.objects.all()
    total = len(all_products)
    processed = 0
    
    for i in range(0, total, batch_size):
        batch = all_products[i:i + batch_size]
        
        # Process each item in the batch
        for product in batch:
            # Example: Update slug based on name
            if not product.slug:
                product.slug = product.name.lower().replace(' ', '-')
                product.save()
                
            processed += 1
            
            # Progress reporting
            if processed % 50 == 0:
                percentage = (processed / total) * 100
                print(f"Progress: {processed}/{total} ({percentage:.1f}%)")
        
        # Optional: Add delay to avoid rate limits
        import time
        time.sleep(0.1)
    
    print(f"Completed processing {processed} products")

# Usage
process_large_dataset(batch_size=50)
```

## Advanced Model Patterns

### Model Inheritance (Simulation)

```python
class BaseModel(Model):
    """Base model with common fields."""
    created_date = DateField(default=date.today)
    updated_date = DateField(default=date.today)
    is_active = BooleanField(default=True)
    
    class Meta:
        abstract = True  # This model won't create a sheet

class Product(BaseModel):
    name = StringField(required=True)
    price = IntegerField()
    
    class Meta:
        sheet_id = 'products-sheet-id'
        client = client

class User(BaseModel):
    username = StringField(required=True)
    email = StringField()
    
    class Meta:
        sheet_id = 'users-sheet-id'
        client = client

# Both Product and User will have the base fields
```

### Model Methods and Properties

```python
class Order(Model):
    order_number = StringField()
    subtotal = IntegerField()
    tax_rate = DecimalField(max_digits=4, decimal_places=4, default=0.0825)
    shipping = IntegerField(default=0)
    
    class Meta:
        sheet_id = 'orders-sheet-id'
        client = client
    
    @property
    def tax_amount(self):
        """Calculate tax amount."""
        return self.subtotal * self.tax_rate
    
    @property
    def total(self):
        """Calculate total order amount."""
        return self.subtotal + self.tax_amount + self.shipping
    
    def apply_discount(self, percent):
        """Apply discount to order."""
        discount_amount = self.subtotal * (percent / 100)
        self.subtotal = int(self.subtotal - discount_amount)
        return discount_amount
    
    def __str__(self):
        return f"Order {self.order_number}: ${self.total:.2f}"

# Usage
order = Order(order_number="ORD-001", subtotal=100, shipping=10)
print(f"Tax: ${order.tax_amount:.2f}")
print(f"Total: ${order.total:.2f}")

discount = order.apply_discount(10)  # 10% discount
print(f"Applied ${discount:.2f} discount")
```

### Model Validation

```python
from sheetalchemy.exceptions import ValidationError

class User(Model):
    username = StringField(required=True)
    email = StringField(required=True)
    age = IntegerField()
    
    class Meta:
        sheet_id = 'users-sheet-id'
        client = client
    
    def clean(self):
        """Custom validation logic."""
        # Validate email format
        if self.email and '@' not in self.email:
            raise ValidationError("Invalid email format")
        
        # Validate age
        if self.age is not None and self.age < 0:
            raise ValidationError("Age cannot be negative")
        
        # Username constraints
        if self.username and len(self.username) < 3:
            raise ValidationError("Username must be at least 3 characters")
    
    def save(self, *args, **kwargs):
        """Override save to include validation."""
        self.clean()  # Run validation
        return super().save(*args, **kwargs)

# Usage with error handling
try:
    user = User(username="ab", email="invalid-email", age=-5)
    user.save()  # Will raise ValidationError
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Performance Optimization

### Caching Strategies

```python
from functools import lru_cache
import time

class CachedProductManager(Manager):
    """Manager with caching for expensive queries."""
    
    def __init__(self):
        super().__init__()
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
    
    def _get_cache_key(self, method, *args, **kwargs):
        """Generate cache key."""
        return f"{method}:{hash(str(args) + str(sorted(kwargs.items())))}"
    
    def _get_cached(self, key):
        """Get value from cache if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._cache_timeout:
                return value
            else:
                del self._cache[key]
        return None
    
    def _set_cache(self, key, value):
        """Set value in cache."""
        self._cache[key] = (value, time.time())
    
    def get_categories(self):
        """Get all unique categories (cached)."""
        cache_key = self._get_cache_key('categories')
        cached = self._get_cached(cache_key)
        
        if cached is not None:
            return cached
        
        products = self.all()
        categories = list(set(p.category for p in products if p.category))
        categories.sort()
        
        self._set_cache(cache_key, categories)
        return categories
    
    @lru_cache(maxsize=128)
    def count_by_category(self, category):
        """Count products in category (LRU cached)."""
        return len(self.filter(category=category))

class Product(Model):
    name = StringField()
    category = StringField()
    
    objects = CachedProductManager()
    
    class Meta:
        sheet_id = 'products-sheet-id'
        client = client

# Usage
categories = Product.objects.get_categories()  # Cached for 5 minutes
count = Product.objects.count_by_category('Electronics')  # LRU cached
```

### Connection Management

```python
class ConnectionManager:
    """Manage Google Sheets API connections efficiently."""
    
    def __init__(self):
        self._clients = {}
        self._connection_timeout = 3600  # 1 hour
    
    def get_client(self, service_account_file):
        """Get or create client connection."""
        if service_account_file not in self._clients:
            from sheetalchemy import authenticate
            self._clients[service_account_file] = {
                'client': authenticate(service_account_file),
                'created': time.time()
            }
        
        return self._clients[service_account_file]['client']
    
    def cleanup_old_connections(self):
        """Remove old connections."""
        current_time = time.time()
        to_remove = []
        
        for key, conn_info in self._clients.items():
            if current_time - conn_info['created'] > self._connection_timeout:
                to_remove.append(key)
        
        for key in to_remove:
            del self._clients[key]

# Global connection manager
connection_manager = ConnectionManager()

# Use in models
class Product(Model):
    name = StringField()
    
    class Meta:
        sheet_id = 'products-sheet-id'
        client = connection_manager.get_client('service-account.json')
```

### Memory Optimization for Large Datasets

```python
def process_large_dataset_memory_efficient(model_class):
    """Process large datasets without loading everything into memory."""
    
    # Get total count first
    total_count = len(model_class.objects.all())
    batch_size = 100
    processed = 0
    
    for offset in range(0, total_count, batch_size):
        # Process in batches
        batch = model_class.objects.all()[offset:offset + batch_size]
        
        for item in batch:
            # Process individual item
            yield item
            processed += 1
            
            if processed % 500 == 0:
                print(f"Processed {processed}/{total_count}")
        
        # Clear batch from memory
        del batch

# Usage
for product in process_large_dataset_memory_efficient(Product):
    # Process each product individually
    if product.price > 1000:
        product.is_premium = True
        product.save()
```

## Integration Patterns

### Flask Integration

```python
from flask import Flask, jsonify, request
from sheetalchemy.exceptions import ValidationError

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products with optional filtering."""
    try:
        # Parse query parameters
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        
        # Build query
        queryset = Product.objects.all()
        
        if category:
            queryset = queryset.filter(category=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Convert to JSON-serializable format
        products = []
        for product in queryset:
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category
            })
        
        return jsonify({
            'success': True,
            'data': products,
            'count': len(products)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product."""
    try:
        data = request.get_json()
        
        product = Product(
            name=data.get('name'),
            price=data.get('price'),
            category=data.get('category')
        )
        product.save()
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'id': product.id
        }), 201
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': f'Validation error: {e}'
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Django Integration

```python
# In Django views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def product_api(request):
    """Django view for product API."""
    
    if request.method == 'GET':
        try:
            # Get query parameters
            category = request.GET.get('category')
            
            # Query products
            products = Product.objects.all()
            if category:
                products = products.filter(category=category)
            
            # Serialize
            data = [
                {
                    'id': p.id,
                    'name': p.name,
                    'price': p.price,
                    'category': p.category
                }
                for p in products
            ]
            
            return JsonResponse({'success': True, 'data': data})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            product = Product(
                name=data.get('name'),
                price=data.get('price'),
                category=data.get('category')
            )
            product.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Product created',
                'id': product.id
            }, status=201)
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

# In Django urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/products/', views.product_api, name='product_api'),
]
```

### Background Tasks with Celery

```python
# tasks.py
from celery import Celery
from datetime import date

app = Celery('godm_tasks')

@app.task
def sync_products_daily():
    """Daily product synchronization task."""
    try:
        # Get products that need updates
        products = Product.objects.filter(
            last_updated__lt=date.today()
        )
        
        updated_count = 0
        for product in products:
            # Perform some update logic
            product.last_updated = date.today()
            product.save()
            updated_count += 1
        
        return f"Updated {updated_count} products"
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.task
def generate_report():
    """Generate product report."""
    try:
        products = Product.objects.all()
        
        report = {
            'total_products': len(products),
            'categories': {},
            'price_ranges': {
                'budget': 0,      # < $100
                'mid_range': 0,   # $100-$500
                'premium': 0      # > $500
            },
            'generated_at': date.today().isoformat()
        }
        
        for product in products:
            # Category counts
            cat = product.category or 'Uncategorized'
            report['categories'][cat] = report['categories'].get(cat, 0) + 1
            
            # Price ranges
            if product.price < 100:
                report['price_ranges']['budget'] += 1
            elif product.price <= 500:
                report['price_ranges']['mid_range'] += 1
            else:
                report['price_ranges']['premium'] += 1
        
        return report
    
    except Exception as e:
        return {'error': str(e)}

# Schedule tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    'sync-products-daily': {
        'task': 'tasks.sync_products_daily',
        'schedule': crontab(hour=2, minute=0),  # Run at 2 AM daily
    },
    'generate-report-weekly': {
        'task': 'tasks.generate_report',
        'schedule': crontab(day_of_week=1, hour=8, minute=0),  # Mondays at 8 AM
    },
}
```

## Error Handling and Logging

### Comprehensive Error Handling

```python
import logging
from sheetalchemy.exceptions import ValidationError, SheetNotFoundError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustProductManager(Manager):
    """Manager with comprehensive error handling."""
    
    def safe_get(self, **kwargs):
        """Safely get a single object."""
        try:
            return self.filter(**kwargs).first()
        except SheetNotFoundError:
            logger.error(f"Sheet not found when querying with {kwargs}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in safe_get: {e}")
            return None
    
    def safe_create(self, **kwargs):
        """Safely create an object."""
        try:
            obj = self.model(**kwargs)
            obj.save()
            logger.info(f"Created {self.model.__name__} with {kwargs}")
            return obj
        except ValidationError as e:
            logger.warning(f"Validation error creating {self.model.__name__}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating {self.model.__name__}: {e}")
            return None
    
    def safe_bulk_create(self, objects_data):
        """Safely create multiple objects."""
        created = []
        errors = []
        
        for i, data in enumerate(objects_data):
            try:
                obj = self.model(**data)
                obj.save()
                created.append(obj)
                logger.info(f"Created object {i+1}/{len(objects_data)}")
            except Exception as e:
                errors.append({'index': i, 'data': data, 'error': str(e)})
                logger.warning(f"Failed to create object {i+1}: {e}")
        
        return {
            'created': created,
            'errors': errors,
            'success_count': len(created),
            'error_count': len(errors)
        }

class Product(Model):
    name = StringField(required=True)
    price = IntegerField()
    
    objects = RobustProductManager()
    
    class Meta:
        sheet_id = 'products-sheet-id'
        client = client

# Usage
product = Product.objects.safe_get(name="Laptop")
if product:
    print(f"Found: {product.name}")
else:
    print("Product not found or error occurred")
```

## Testing SheetAlchemy Applications

### Unit Testing

```python
import unittest
from unittest.mock import Mock, patch
from sheetalchemy import Model, StringField, IntegerField

class TestProduct(unittest.TestCase):
    """Test Product model."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the Google Sheets client
        self.mock_client = Mock()
        
        # Create test model
        class TestProduct(Model):
            name = StringField()
            price = IntegerField()
            
            class Meta:
                sheet_id = 'test-sheet'
                client = self.mock_client
        
        self.Product = TestProduct
    
    def test_product_creation(self):
        """Test product creation."""
        product = self.Product(name="Test Product", price=100)
        
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100)
    
    @patch('godm.model.gspread')
    def test_product_save(self, mock_gspread):
        """Test product saving."""
        # Mock the save operation
        mock_worksheet = Mock()
        mock_gspread.return_value.open_by_key.return_value.worksheet.return_value = mock_worksheet
        
        product = self.Product(name="Test Product", price=100)
        product.save()
        
        # Verify save was called
        self.assertTrue(mock_worksheet.append_row.called or mock_worksheet.update.called)
    
    def test_product_validation(self):
        """Test product validation."""
        # Test required field validation
        with self.assertRaises(Exception):
            product = self.Product(price=100)  # Missing required name
            product.save()

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
import pytest
from sheetalchemy import authenticate
import os

@pytest.fixture
def test_client():
    """Create test client."""
    # Use test service account
    service_account_file = os.getenv('TEST_SERVICE_ACCOUNT_FILE')
    return authenticate(service_account_file)

@pytest.fixture
def test_product_model(test_client):
    """Create test product model."""
    class TestProduct(Model):
        name = StringField()
        price = IntegerField()
        
        class Meta:
            sheet_id = os.getenv('TEST_SHEET_ID')
            client = test_client
    
    return TestProduct

def test_full_crud_operations(test_product_model):
    """Test complete CRUD operations."""
    Product = test_product_model
    
    # Create
    product = Product(name="Integration Test Product", price=999)
    product.save()
    assert product.id is not None
    
    # Read
    found_product = Product.objects.filter(name="Integration Test Product").first()
    assert found_product is not None
    assert found_product.price == 999
    
    # Update
    found_product.price = 1099
    found_product.save()
    
    # Verify update
    updated_product = Product.objects.filter(id=found_product.id).first()
    assert updated_product.price == 1099
    
    # Delete
    updated_product.delete()
    
    # Verify deletion
    deleted_product = Product.objects.filter(id=updated_product.id).first()
    assert deleted_product is None
```

## Next Steps

You've now learned advanced SheetAlchemy patterns! Here's what to explore next:

1. **Build a complete application**: Try the examples in the `examples/` directory
2. **Contribute to SheetAlchemy**: Check out the [Contributing Guide](../CONTRIBUTING.md)
3. **Performance tuning**: Optimize your specific use cases
4. **Integration patterns**: Adapt SheetAlchemy to your application architecture
5. **Community**: Share your experiences and learn from others

## Advanced Tips Summary

- **Use custom managers** for reusable query methods
- **Implement data transformers** for automatic data formatting
- **Optimize with caching** for frequently accessed data
- **Handle errors gracefully** with comprehensive exception handling
- **Test thoroughly** with both unit and integration tests
- **Monitor performance** when working with large datasets
- **Document your code** for maintainability

Happy building with SheetAlchemy! 🚀