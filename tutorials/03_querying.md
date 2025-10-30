# Querying and Filtering Tutorial

G-ODM provides a powerful Django-inspired querying API that allows you to filter, sort, and manipulate your Google Sheets data with ease.

## Basic Querying

### Getting All Records

```python
from godm import Model, StringField, IntegerField

class Product(Model):
    name = StringField()
    price = IntegerField()
    category = StringField()
    
    class Meta:
        sheet_id = 'your-sheet-id'
        client = client

# Get all products
all_products = Product.objects.all()
print(f"Total products: {len(all_products)}")

# Iterate through results
for product in all_products:
    print(f"{product.name}: ${product.price}")
```

### Getting Single Records

```python
# Get the first record
first_product = Product.objects.first()

# Get the last record  
last_product = Product.objects.last()

# Get a specific record by index
third_product = Product.objects.all()[2]

# Get one record with filter (returns None if not found)
expensive_product = Product.objects.filter(price__gt=1000).first()
```

## Filtering with Lookups

G-ODM supports various lookup types for filtering data:

### Exact Match

```python
# Exact match (case-sensitive)
laptops = Product.objects.filter(category="Electronics")

# Case-insensitive exact match
laptops_ci = Product.objects.filter(category__iexact="electronics")
```

### Comparison Operators

```python
# Greater than
expensive = Product.objects.filter(price__gt=500)

# Greater than or equal
mid_range = Product.objects.filter(price__gte=200)

# Less than
budget = Product.objects.filter(price__lt=100)

# Less than or equal
affordable = Product.objects.filter(price__lte=300)

# Not equal
not_electronics = Product.objects.filter(category__ne="Electronics")
```

### String Operations

```python
# Contains substring (case-sensitive)
phone_products = Product.objects.filter(name__contains="Phone")

# Case-insensitive contains
phone_products_ci = Product.objects.filter(name__icontains="phone")

# Starts with
apple_products = Product.objects.filter(name__startswith="Apple")

# Case-insensitive starts with
apple_products_ci = Product.objects.filter(name__istartswith="apple")

# Ends with
pro_products = Product.objects.filter(name__endswith="Pro")

# Case-insensitive ends with
pro_products_ci = Product.objects.filter(name__iendswith="pro")
```

### List Operations

```python
# In a list of values
categories = Product.objects.filter(category__in=["Electronics", "Books", "Clothing"])

# Not in a list
not_categories = Product.objects.filter(category__not_in=["Electronics", "Books"])
```

### Null/Empty Checks

```python
# Field is null/empty
no_description = Product.objects.filter(description__isnull=True)

# Field is not null/empty
has_description = Product.objects.filter(description__isnull=False)

# Field is blank (empty string)
blank_notes = Product.objects.filter(notes__exact="")
```

## Complex Filtering

### Multiple Conditions (AND)

```python
# Multiple filters are combined with AND
expensive_electronics = Product.objects.filter(
    category="Electronics",
    price__gt=500
)

# Alternative syntax
expensive_electronics = Product.objects.filter(
    category="Electronics"
).filter(
    price__gt=500
)
```

### OR Conditions

```python
from godm import Q

# Use Q objects for OR conditions
phones_or_tablets = Product.objects.filter(
    Q(category="Phones") | Q(category="Tablets")
)

# Complex OR with AND
expensive_phones_or_cheap_tablets = Product.objects.filter(
    (Q(category="Phones") & Q(price__gt=800)) | 
    (Q(category="Tablets") & Q(price__lt=300))
)
```

### NOT Conditions

```python
# Exclude specific conditions
not_electronics = Product.objects.exclude(category="Electronics")

# Using Q with NOT
not_expensive = Product.objects.filter(~Q(price__gt=1000))

# Combine exclude with filter
cheap_non_electronics = Product.objects.filter(
    price__lt=100
).exclude(
    category="Electronics"
)
```

## Sorting and Ordering

### Basic Ordering

```python
# Order by single field (ascending)
by_price = Product.objects.order_by('price')

# Order by single field (descending)
by_price_desc = Product.objects.order_by('-price')

# Order by multiple fields
by_category_then_price = Product.objects.order_by('category', 'price')

# Mix ascending and descending
mixed_order = Product.objects.order_by('category', '-price')
```

### Advanced Ordering

```python
# Order by string length
by_name_length = Product.objects.order_by('name__len')

# Case-insensitive ordering
by_name_ci = Product.objects.order_by('name__lower')

# Random ordering (useful for sampling)
random_products = Product.objects.order_by('?')
```

## Chaining Operations

You can chain filtering, ordering, and other operations:

```python
# Chain multiple operations
expensive_electronics_by_name = (
    Product.objects
    .filter(category="Electronics")
    .filter(price__gt=500)
    .order_by('name')
    .exclude(name__contains="Refurbished")
)

# Each method returns a new QuerySet
electronics = Product.objects.filter(category="Electronics")
expensive_electronics = electronics.filter(price__gt=500)
sorted_expensive = expensive_electronics.order_by('-price')
```

## Slicing and Pagination

### Basic Slicing

```python
# Get first 5 products
first_five = Product.objects.all()[:5]

# Get products 10-20
products_10_to_20 = Product.objects.all()[10:20]

# Get every other product
every_other = Product.objects.all()[::2]

# Get last 5 products (requires ordering)
last_five = Product.objects.order_by('-id')[:5]
```

### Pagination Helper

```python
def paginate_products(page=1, per_page=10):
    """Simple pagination helper."""
    start = (page - 1) * per_page
    end = start + per_page
    
    products = Product.objects.order_by('name')[start:end]
    total = len(Product.objects.all())
    
    return {
        'products': products,
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page
    }

# Usage
page_1 = paginate_products(page=1, per_page=10)
for product in page_1['products']:
    print(product.name)
```

## Aggregation and Counting

### Counting Records

```python
# Count all records
total_products = Product.objects.count()

# Count filtered records
electronics_count = Product.objects.filter(category="Electronics").count()

# Check if any records exist
has_products = Product.objects.exists()
has_expensive = Product.objects.filter(price__gt=1000).exists()
```

### Simple Aggregation

```python
def calculate_stats():
    """Calculate product statistics."""
    products = Product.objects.all()
    
    if not products:
        return None
    
    prices = [p.price for p in products if p.price]
    
    return {
        'total_products': len(products),
        'avg_price': sum(prices) / len(prices) if prices else 0,
        'max_price': max(prices) if prices else 0,
        'min_price': min(prices) if prices else 0,
        'categories': len(set(p.category for p in products if p.category))
    }

# Usage
stats = calculate_stats()
print(f"Average price: ${stats['avg_price']:.2f}")
```

## Advanced Query Patterns

### Dynamic Filtering

```python
def search_products(name=None, category=None, min_price=None, max_price=None):
    """Dynamic product search with optional filters."""
    queryset = Product.objects.all()
    
    if name:
        queryset = queryset.filter(name__icontains=name)
    
    if category:
        queryset = queryset.filter(category=category)
    
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    
    return queryset.order_by('name')

# Usage
results = search_products(name="phone", min_price=200, max_price=800)
```

### Building Complex Queries

```python
from godm import Q

def advanced_product_search(query_params):
    """Build complex queries from parameters."""
    queryset = Product.objects.all()
    
    # Text search across multiple fields
    if 'search' in query_params:
        search_term = query_params['search']
        queryset = queryset.filter(
            Q(name__icontains=search_term) | 
            Q(description__icontains=search_term) |
            Q(category__icontains=search_term)
        )
    
    # Price range
    if 'price_range' in query_params:
        min_price, max_price = query_params['price_range']
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
    
    # Multiple categories
    if 'categories' in query_params:
        queryset = queryset.filter(category__in=query_params['categories'])
    
    # Exclude discontinued
    if query_params.get('exclude_discontinued'):
        queryset = queryset.exclude(status="discontinued")
    
    return queryset

# Usage
search_params = {
    'search': 'phone',
    'price_range': (200, 800),
    'categories': ['Electronics', 'Mobile'],
    'exclude_discontinued': True
}
results = advanced_product_search(search_params)
```

### Query Performance Tips

```python
# Good: Filter before ordering and slicing
efficient_query = (
    Product.objects
    .filter(category="Electronics")  # Reduce dataset first
    .filter(price__gt=100)          # Further filtering
    .order_by('price')              # Then order
    [:10]                           # Finally limit
)

# Less efficient: Order everything then filter
inefficient_query = (
    Product.objects
    .order_by('price')              # Orders all records
    .filter(category="Electronics") # Then filters
    [:10]
)

# Cache frequently used queries
class ProductQueries:
    @staticmethod
    def popular_electronics():
        return Product.objects.filter(
            category="Electronics",
            rating__gte=4
        ).order_by('-sales_count')
    
    @staticmethod
    def budget_items():
        return Product.objects.filter(
            price__lt=50
        ).order_by('price')
```

## Working with Dates

```python
from datetime import date, timedelta
from godm import DateField

class Order(Model):
    order_date = DateField()
    customer = StringField()
    total = DecimalField()

# Date filtering
today = date.today()
yesterday = today - timedelta(days=1)
last_week = today - timedelta(weeks=1)

# Orders from today
todays_orders = Order.objects.filter(order_date=today)

# Orders from this week
this_week = Order.objects.filter(order_date__gte=last_week)

# Orders from a specific month
from datetime import datetime
january_2024 = Order.objects.filter(
    order_date__gte=date(2024, 1, 1),
    order_date__lt=date(2024, 2, 1)
)

# Recent orders (last 30 days)
recent = Order.objects.filter(
    order_date__gte=today - timedelta(days=30)
).order_by('-order_date')
```

## Common Query Patterns

### Finding Duplicates

```python
def find_duplicate_products():
    """Find products with duplicate names."""
    products = Product.objects.all()
    names = {}
    
    for product in products:
        name = product.name.lower()
        if name in names:
            names[name].append(product)
        else:
            names[name] = [product]
    
    # Return only duplicates
    return {name: products for name, products in names.items() if len(products) > 1}

# Usage
duplicates = find_duplicate_products()
for name, products in duplicates.items():
    print(f"Duplicate name '{name}':")
    for product in products:
        print(f"  - ID: {product.id}, Price: {product.price}")
```

### Top N Queries

```python
def get_top_products(category=None, limit=10):
    """Get top products by price in a category."""
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    
    return queryset.order_by('-price')[:limit]

# Usage
top_electronics = get_top_products(category="Electronics", limit=5)
```

### Batch Processing

```python
def process_products_in_batches(batch_size=100):
    """Process products in batches to avoid memory issues."""
    all_products = Product.objects.all()
    total = len(all_products)
    
    for i in range(0, total, batch_size):
        batch = all_products[i:i + batch_size]
        
        # Process each batch
        for product in batch:
            # Do something with product
            if product.price < 10:
                product.category = "Clearance"
                product.save()
        
        print(f"Processed batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}")

# Usage
process_products_in_batches(batch_size=50)
```

## Query Optimization Tips

### 1. Use Specific Filters

```python
# Good: Specific filters
expensive_phones = Product.objects.filter(
    category="Phones",
    price__gt=500
)

# Less efficient: Get all then filter in Python
all_products = Product.objects.all()
expensive_phones = [p for p in all_products if p.category == "Phones" and p.price > 500]
```

### 2. Order Your Filters

```python
# Good: Most selective filters first
results = Product.objects.filter(
    price__gt=1000,        # Highly selective
    category="Electronics", # Less selective
    name__contains="Pro"   # Least selective
)
```

### 3. Use exists() for Checks

```python
# Good: Use exists() for boolean checks
if Product.objects.filter(category="Electronics").exists():
    print("We have electronics!")

# Less efficient: Count or convert to list
if len(Product.objects.filter(category="Electronics")) > 0:
    print("We have electronics!")
```

### 4. Cache Query Results

```python
class ProductCache:
    def __init__(self):
        self._categories = None
        self._category_counts = None
    
    def get_categories(self):
        if self._categories is None:
            products = Product.objects.all()
            self._categories = list(set(p.category for p in products if p.category))
        return self._categories
    
    def get_category_counts(self):
        if self._category_counts is None:
            products = Product.objects.all()
            counts = {}
            for product in products:
                if product.category:
                    counts[product.category] = counts.get(product.category, 0) + 1
            self._category_counts = counts
        return self._category_counts
    
    def clear_cache(self):
        self._categories = None
        self._category_counts = None

# Usage
cache = ProductCache()
categories = cache.get_categories()  # Cached after first call
```

## Error Handling

```python
from godm.exceptions import ValidationError, SheetNotFoundError

def safe_query_products(filters=None):
    """Safely query products with error handling."""
    try:
        queryset = Product.objects.all()
        
        if filters:
            for field, value in filters.items():
                queryset = queryset.filter(**{field: value})
        
        return {
            'success': True,
            'data': list(queryset),
            'count': len(queryset)
        }
    
    except SheetNotFoundError:
        return {
            'success': False,
            'error': 'Product sheet not found. Please check sheet configuration.',
            'data': [],
            'count': 0
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Query failed: {str(e)}',
            'data': [],
            'count': 0
        }

# Usage
result = safe_query_products({'category': 'Electronics', 'price__gt': 100})
if result['success']:
    for product in result['data']:
        print(product.name)
else:
    print(f"Error: {result['error']}")
```

## Query Reference

### All Available Lookups

```python
# Exact matching
field__exact="value"        # Exact match
field__iexact="value"       # Case-insensitive exact match

# Comparison
field__gt=value             # Greater than
field__gte=value            # Greater than or equal
field__lt=value             # Less than
field__lte=value            # Less than or equal
field__ne=value             # Not equal

# String operations
field__contains="text"      # Contains substring
field__icontains="text"     # Case-insensitive contains
field__startswith="text"    # Starts with
field__istartswith="text"   # Case-insensitive starts with
field__endswith="text"      # Ends with
field__iendswith="text"     # Case-insensitive ends with

# List operations
field__in=[val1, val2]      # In list
field__not_in=[val1, val2]  # Not in list

# Null checks
field__isnull=True          # Is null/empty
field__isnull=False         # Is not null/empty

# String utilities
field__len=5                # String length equals
field__lower="text"         # Lowercase comparison
```

## Next Steps

Now that you've mastered querying:

1. **Explore advanced features**: Check out the [Advanced Usage Tutorial](04_advanced_usage.md)
2. **See complex examples**: Look at the inventory management example in `examples/`
3. **Learn about model relationships**: Understand how to work with related data
4. **Performance optimization**: Learn best practices for large datasets

Happy querying! 🔍