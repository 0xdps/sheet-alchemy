"""
Advanced Inventory Management System with SheetAlchemy

This example demonstrates advanced SheetAlchemy features:
1. Multiple related models
2. Custom field transformations
3. Complex querying and filtering
4. Data aggregation and reporting
5. Error handling and validation
6. Load policies and performance optimization

Required Google Sheets structure:

Sheet Name: "Inventory Management System"

Tab 1 - "Products":
ID | Name | Category | Price | Quantity | Min Stock | Supplier | Last Updated | Tags | Active

Tab 2 - "Categories":  
ID | Name | Description | Tax Rate | Active

Tab 3 - "Suppliers":
ID | Name | Contact Email | Phone | Address | Rating | Active

Sample Products data:
1 | Laptop Pro 15"     | Electronics | 1299.99 | 25 | 10 | TechCorp     | 10/15/2024 | laptop,computer,premium | TRUE
2 | Wireless Mouse     | Electronics | 29.99   | 150| 20 | TechCorp     | 10/14/2024 | mouse,wireless,office   | TRUE  
3 | Office Chair       | Furniture   | 249.99  | 8  | 5  | ComfortSeats | 10/13/2024 | chair,office,ergonomic  | TRUE
4 | USB Cable          | Electronics | 12.99   | 200| 50 | TechCorp     | 10/12/2024 | cable,usb,accessory     | TRUE
5 | Standing Desk      | Furniture   | 599.99  | 3  | 2  | ComfortSeats | 10/11/2024 | desk,standing,office    | FALSE
"""

import os
from datetime import datetime, timedelta
from sheetalchemy import LoadPolicy
from godm.field import (
    StringField, IntegerField, DateField, BooleanField, 
    DecimalField, ListField, CustomField
)
from godm.model import GModel
from godm._auth import authenticate
from godm.exceptions import ModelItemException, FieldException


# Custom transformations for advanced functionality
def calculate_stock_status(data):
    """Custom field to calculate stock status based on quantity and minimum stock."""
    try:
        quantity = int(data.get("Quantity", 0))
        min_stock = int(data.get("Min Stock", 0))
        
        if quantity <= 0:
            return "OUT_OF_STOCK"
        elif quantity <= min_stock:
            return "LOW_STOCK" 
        elif quantity <= min_stock * 2:
            return "NORMAL_STOCK"
        else:
            return "HIGH_STOCK"
    except (ValueError, TypeError):
        return "UNKNOWN"


def calculate_stock_value(data):
    """Custom field to calculate total value of stock."""
    try:
        price = float(data.get("Price", 0))
        quantity = int(data.get("Quantity", 0))
        return round(price * quantity, 2)
    except (ValueError, TypeError):
        return 0.0


def days_since_update(data):
    """Custom field to calculate days since last update."""
    try:
        last_updated_str = data.get("Last Updated", "")
        if not last_updated_str:
            return 999  # Very old if no date
            
        last_updated = datetime.strptime(last_updated_str, "%m/%d/%Y")
        days_diff = (datetime.now() - last_updated).days
        return days_diff
    except (ValueError, TypeError):
        return 999


# Model Definitions
class Product(GModel):
    """Product model with advanced field types and custom calculations."""
    
    id = IntegerField(name="ID")
    name = StringField(name="Name")
    category = StringField(name="Category")
    price = DecimalField(name="Price", allow_empty_or_null=False)
    quantity = IntegerField(name="Quantity", default_val=0)
    min_stock = IntegerField(name="Min Stock", default_val=0)
    supplier = StringField(name="Supplier", allow_empty_or_null=True, default_val="Unknown")
    last_updated = DateField(name="Last Updated", format=DateField.MM_DD_YYYY)
    tags = ListField(name="Tags", delimiter=",", item_type=str, allow_empty_or_null=True)
    is_active = BooleanField(name="Active", default_val=True)
    
    # Custom calculated fields
    stock_status = CustomField(to_value=calculate_stock_status)
    stock_value = CustomField(to_value=calculate_stock_value)
    days_since_update = CustomField(to_value=days_since_update)
    
    class Meta:
        sheet_name = "Inventory Management System"
        tab_name = "Products"
        header_index = 1
        load_policy = LoadPolicy.LAZY


class Category(GModel):
    """Category model for organizing products."""
    
    id = IntegerField(name="ID")
    name = StringField(name="Name")
    description = StringField(name="Description", allow_empty_or_null=True, default_val="")
    tax_rate = DecimalField(name="Tax Rate", allow_empty_or_null=True, default_val=0.0)
    is_active = BooleanField(name="Active", default_val=True)
    
    class Meta:
        sheet_name = "Inventory Management System"
        tab_name = "Categories"
        header_index = 1
        load_policy = LoadPolicy.INIT  # Load immediately for reference data


class Supplier(GModel):
    """Supplier model for vendor management."""
    
    id = IntegerField(name="ID")
    name = StringField(name="Name")
    contact_email = StringField(name="Contact Email", allow_empty_or_null=True)
    phone = StringField(name="Phone", allow_empty_or_null=True)
    address = StringField(name="Address", allow_empty_or_null=True)
    rating = DecimalField(name="Rating", allow_empty_or_null=True, default_val=5.0)
    is_active = BooleanField(name="Active", default_val=True)
    
    class Meta:
        sheet_name = "Inventory Management System" 
        tab_name = "Suppliers"
        header_index = 1
        load_policy = LoadPolicy.INIT


class InventoryManager:
    """Advanced inventory management operations."""
    
    def __init__(self):
        self.products = Product
        self.categories = Category
        self.suppliers = Supplier
    
    def get_low_stock_products(self):
        """Get products that are low on stock."""
        low_stock = []
        for product in self.products.manager.filter(is_active=True):
            if product.stock_status in ["LOW_STOCK", "OUT_OF_STOCK"]:
                low_stock.append(product)
        return low_stock
    
    def get_high_value_products(self, min_value=1000):
        """Get products with high stock value."""
        high_value = []
        for product in self.products.manager.filter(is_active=True):
            if product.stock_value >= min_value:
                high_value.append(product)
        return high_value
    
    def get_products_by_category(self, category_name):
        """Get all products in a specific category."""
        return self.products.manager.filter(category=category_name, is_active=True)
    
    def get_products_by_supplier(self, supplier_name):
        """Get all products from a specific supplier."""
        return self.products.manager.filter(supplier=supplier_name, is_active=True)
    
    def get_stale_products(self, days_threshold=30):
        """Get products not updated recently."""
        stale_products = []
        for product in self.products.manager.filter(is_active=True):
            if product.days_since_update > days_threshold:
                stale_products.append(product)
        return stale_products
    
    def generate_inventory_report(self):
        """Generate comprehensive inventory report."""
        all_products = list(self.products.manager.filter(is_active=True))
        
        report = {
            "total_products": len(all_products),
            "total_value": sum(p.stock_value for p in all_products),
            "low_stock_count": len([p for p in all_products if p.stock_status == "LOW_STOCK"]),
            "out_of_stock_count": len([p for p in all_products if p.stock_status == "OUT_OF_STOCK"]),
            "categories": {},
            "suppliers": {},
            "stock_status_distribution": {}
        }
        
        # Category breakdown
        for product in all_products:
            category = product.category
            if category not in report["categories"]:
                report["categories"][category] = {"count": 0, "value": 0}
            report["categories"][category]["count"] += 1
            report["categories"][category]["value"] += product.stock_value
        
        # Supplier breakdown  
        for product in all_products:
            supplier = product.supplier
            if supplier not in report["suppliers"]:
                report["suppliers"][supplier] = {"count": 0, "value": 0}
            report["suppliers"][supplier]["count"] += 1
            report["suppliers"][supplier]["value"] += product.stock_value
        
        # Stock status distribution
        for product in all_products:
            status = product.stock_status
            report["stock_status_distribution"][status] = report["stock_status_distribution"].get(status, 0) + 1
        
        return report
    
    def search_products(self, query):
        """Search products by name or tags."""
        results = []
        
        # Search by name
        try:
            name_results = self.products.manager.filter(name__ct=query, is_active=True)
            results.extend(list(name_results))
        except:
            pass
        
        # Search by tags
        for product in self.products.manager.filter(is_active=True):
            if query.lower() in [tag.lower() for tag in product.tags]:
                if product not in results:
                    results.append(product)
        
        return results


def setup_authentication():
    """Set up authentication for the inventory system."""
    auth_key_path = os.getenv('GODM_AUTH_KEY_PATH')
    if auth_key_path and os.path.exists(auth_key_path):
        authenticate(key_path=auth_key_path)
        return True
    
    print("❌ Authentication setup required:")
    print("1. Set GODM_AUTH_KEY_PATH environment variable")
    print("2. Ensure your service account has access to the sheets")
    return False


def demonstrate_basic_operations(inventory):
    """Demonstrate basic inventory operations."""
    print("\n🛍️ === Basic Inventory Operations ===")
    
    try:
        # Get all active products
        all_products = list(inventory.products.manager.filter(is_active=True))
        print(f"\n📦 Total active products: {len(all_products)}")
        
        # Show first few products with details
        print("\nSample products:")
        for i, product in enumerate(all_products[:3]):
            print(f"\n  {i+1}. {product.name}")
            print(f"     Category: {product.category}")
            print(f"     Price: ${product.price}")
            print(f"     Stock: {product.quantity} (Min: {product.min_stock})")
            print(f"     Status: {product.stock_status}")
            print(f"     Value: ${product.stock_value}")
            print(f"     Supplier: {product.supplier}")
            print(f"     Tags: {product.tags}")
        
        if len(all_products) > 3:
            print(f"     ... and {len(all_products) - 3} more products")
            
    except Exception as e:
        print(f"❌ Error in basic operations: {e}")


def demonstrate_stock_management(inventory):
    """Demonstrate stock management features."""
    print("\n📊 === Stock Management ===")
    
    try:
        # Low stock alerts
        low_stock = inventory.get_low_stock_products()
        print(f"\n⚠️  Low stock alerts: {len(low_stock)} products")
        for product in low_stock[:5]:
            print(f"   - {product.name}: {product.quantity} units ({product.stock_status})")
        
        # High value inventory
        high_value = inventory.get_high_value_products(min_value=500)
        print(f"\n💰 High-value products (>$500): {len(high_value)} products")
        for product in high_value[:3]:
            print(f"   - {product.name}: ${product.stock_value}")
        
        # Stale inventory
        stale_products = inventory.get_stale_products(days_threshold=7)
        print(f"\n📅 Products not updated in 7+ days: {len(stale_products)}")
        for product in stale_products[:3]:
            print(f"   - {product.name}: {product.days_since_update} days ago")
            
    except Exception as e:
        print(f"❌ Error in stock management: {e}")


def demonstrate_category_analysis(inventory):
    """Demonstrate category-based analysis."""
    print("\n🏷️ === Category Analysis ===")
    
    try:
        # Get all categories
        categories = list(inventory.categories.manager.filter(is_active=True))
        print(f"\nActive categories: {len(categories)}")
        
        for category in categories:
            products_in_category = inventory.get_products_by_category(category.name)
            total_value = sum(p.stock_value for p in products_in_category)
            
            print(f"\n📂 {category.name}")
            print(f"   Description: {category.description}")
            print(f"   Tax Rate: {category.tax_rate}%")
            print(f"   Products: {products_in_category.size()}")
            print(f"   Total Value: ${total_value:,.2f}")
            
            # Show top products in this category
            category_products = list(products_in_category)
            category_products.sort(key=lambda p: p.stock_value, reverse=True)
            print(f"   Top products:")
            for product in category_products[:3]:
                print(f"     - {product.name}: ${product.stock_value}")
                
    except Exception as e:
        print(f"❌ Error in category analysis: {e}")


def demonstrate_supplier_analysis(inventory):
    """Demonstrate supplier-based analysis."""
    print("\n🏢 === Supplier Analysis ===")
    
    try:
        # Get all suppliers
        suppliers = list(inventory.suppliers.manager.filter(is_active=True))
        print(f"\nActive suppliers: {len(suppliers)}")
        
        for supplier in suppliers:
            products_from_supplier = inventory.get_products_by_supplier(supplier.name)
            total_value = sum(p.stock_value for p in products_from_supplier)
            
            print(f"\n🏭 {supplier.name}")
            print(f"   Rating: {supplier.rating}/10")
            print(f"   Contact: {supplier.contact_email}")
            print(f"   Products: {products_from_supplier.size()}")
            print(f"   Total Value: ${total_value:,.2f}")
            
            # Check for low stock from this supplier
            low_stock_from_supplier = [
                p for p in products_from_supplier 
                if p.stock_status in ["LOW_STOCK", "OUT_OF_STOCK"]
            ]
            if low_stock_from_supplier:
                print(f"   ⚠️  Low stock items: {len(low_stock_from_supplier)}")
                
    except Exception as e:
        print(f"❌ Error in supplier analysis: {e}")


def demonstrate_search_functionality(inventory):
    """Demonstrate product search features."""
    print("\n🔍 === Search Functionality ===")
    
    try:
        # Search by different terms
        search_terms = ["laptop", "office", "wireless"]
        
        for term in search_terms:
            results = inventory.search_products(term)
            print(f"\n🔎 Search results for '{term}': {len(results)} products")
            
            for product in results[:3]:
                print(f"   - {product.name} ({product.category})")
                print(f"     Tags: {product.tags}")
            
            if len(results) > 3:
                print(f"   ... and {len(results) - 3} more")
                
    except Exception as e:
        print(f"❌ Error in search functionality: {e}")


def demonstrate_reporting(inventory):
    """Demonstrate comprehensive reporting."""
    print("\n📈 === Inventory Reporting ===")
    
    try:
        report = inventory.generate_inventory_report()
        
        print(f"\n📋 Inventory Summary Report")
        print(f"{'='*50}")
        print(f"Total Products: {report['total_products']:,}")
        print(f"Total Inventory Value: ${report['total_value']:,.2f}")
        print(f"Low Stock Products: {report['low_stock_count']}")
        print(f"Out of Stock Products: {report['out_of_stock_count']}")
        
        print(f"\n📊 Stock Status Distribution:")
        for status, count in report['stock_status_distribution'].items():
            percentage = (count / report['total_products']) * 100
            print(f"   {status}: {count} ({percentage:.1f}%)")
        
        print(f"\n🏷️ Category Breakdown:")
        for category, data in report['categories'].items():
            print(f"   {category}: {data['count']} products, ${data['value']:,.2f}")
        
        print(f"\n🏢 Supplier Breakdown:")
        for supplier, data in report['suppliers'].items():
            print(f"   {supplier}: {data['count']} products, ${data['value']:,.2f}")
            
    except Exception as e:
        print(f"❌ Error in reporting: {e}")


def demonstrate_advanced_filtering(inventory):
    """Demonstrate advanced filtering capabilities."""
    print("\n🎯 === Advanced Filtering ===")
    
    try:
        # Price range filtering
        print(f"\n💲 Products under $50:")
        affordable = inventory.products.manager.filter(price__lt=50, is_active=True)
        for product in affordable:
            print(f"   - {product.name}: ${product.price}")
        
        print(f"\n💎 Premium products over $500:")
        premium = inventory.products.manager.filter(price__gt=500, is_active=True)
        for product in premium:
            print(f"   - {product.name}: ${product.price}")
        
        # Complex stock filtering
        print(f"\n📦 High quantity products (>100 units):")
        high_quantity = inventory.products.manager.filter(quantity__gt=100, is_active=True)
        for product in high_quantity:
            print(f"   - {product.name}: {product.quantity} units")
            
    except Exception as e:
        print(f"❌ Error in advanced filtering: {e}")


def main():
    """Main function to run the inventory management example."""
    print("🏭 SheetAlchemy Advanced Inventory Management System")
    print("=" * 60)
    
    # Setup authentication
    if not setup_authentication():
        return
    
    # Initialize inventory manager
    print("\n⚙️  Initializing inventory system...")
    try:
        inventory = InventoryManager()
        
        # Initialize models
        print("   Loading categories...")
        Category.manager.initialise_model()
        
        print("   Loading suppliers...")
        Supplier.manager.initialise_model()
        
        print("   Loading products...")
        Product.manager.initialise_model()
        
        print("✅ Inventory system initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize inventory system: {e}")
        return
    
    # Run demonstrations
    try:
        demonstrate_basic_operations(inventory)
        demonstrate_stock_management(inventory)
        demonstrate_category_analysis(inventory)
        demonstrate_supplier_analysis(inventory)
        demonstrate_search_functionality(inventory)
        demonstrate_advanced_filtering(inventory)
        demonstrate_reporting(inventory)
        
        print("\n🎉 Advanced inventory example completed!")
        print("\n📚 Key features demonstrated:")
        print("- Custom field calculations")
        print("- Multiple related models")
        print("- Advanced querying and filtering")
        print("- Data aggregation and reporting")
        print("- Search functionality")
        print("- Performance optimization with load policies")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()