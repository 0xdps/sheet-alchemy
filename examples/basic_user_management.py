"""
Simple User Management Example with SheetAlchemy

This example demonstrates:
1. Basic model definition
2. Field types usage
3. Authentication setup
4. Simple CRUD operations
5. Filtering and querying

To run this example:
1. Set up Google Sheets with user data
2. Configure authentication
3. Run the script

Required Google Sheet structure:
- Sheet Name: "User Management Demo"
- Tab Name: "Users"
- Headers (Row 1): Name | Age | Email | Active | Department | Join Date | Tags

Sample data:
John Doe        | 28 | john@company.com    | TRUE  | Engineering | 01/15/2022 | python,backend
Jane Smith      | 32 | jane@company.com    | TRUE  | Design      | 03/20/2021 | ui,frontend
Bob Johnson     | 45 | bob@company.com     | FALSE | Marketing   | 11/10/2020 | seo,content
Alice Brown     | 29 | alice@company.com   | TRUE  | Engineering | 07/05/2023 | javascript,react
"""

import os
from datetime import datetime
from sheetalchemy import LoadPolicy
from godm.field import StringField, IntegerField, DateField, BooleanField, ListField
from godm.model import GModel
from godm._auth import authenticate
from godm.exceptions import ModelItemException, FieldException


# Step 1: Define the User model
class User(GModel):
    """User model representing employees in a company."""
    
    # Field definitions with validation and defaults
    name = StringField(
        name="Name",
        allow_empty_or_null=False
    )
    
    age = IntegerField(
        name="Age", 
        allow_empty_or_null=True,
        default_val=0
    )
    
    email = StringField(
        name="Email",
        allow_empty_or_null=True,
        default_val=""
    )
    
    is_active = BooleanField(
        name="Active",
        allow_empty_or_null=True,
        default_val=True
    )
    
    department = StringField(
        name="Department",
        allow_empty_or_null=True,
        default_val="General"
    )
    
    join_date = DateField(
        name="Join Date",
        format=DateField.MM_DD_YYYY,
        allow_empty_or_null=True,
        default_val="01/01/2020"
    )
    
    tags = ListField(
        name="Tags",
        delimiter=",",
        item_type=str,
        allow_empty_or_null=True,
        default_val=[]
    )
    
    class Meta:
        sheet_name = "User Management Demo"
        tab_name = "Users"
        header_index = 1  # Headers are in row 1
        load_policy = LoadPolicy.LAZY  # Load data when needed


def setup_authentication():
    """
    Set up Google Sheets authentication.
    
    You can authenticate in several ways:
    1. Set GODM_AUTH_KEY_PATH environment variable
    2. Pass key file path directly
    3. Pass key object directly
    """
    # Method 1: Using environment variable (recommended)
    auth_key_path = os.getenv('GODM_AUTH_KEY_PATH')
    if auth_key_path:
        authenticate(key_path=auth_key_path)
        print("✅ Authenticated using environment variable")
        return True
    
    # Method 2: Direct key file path (for demo purposes)
    key_path = "path/to/your/service-account-key.json"
    if os.path.exists(key_path):
        authenticate(key_path=key_path)
        print("✅ Authenticated using key file")
        return True
    
    # Method 3: Key object (for CI/CD or secure environments)
    key_object = {
        # Your service account key content here
        # "type": "service_account",
        # "project_id": "your-project-id",
        # ... other key fields
    }
    if key_object.get("type") == "service_account":
        authenticate(key_object=key_object)
        print("✅ Authenticated using key object")
        return True
    
    print("❌ Authentication failed. Please set up your credentials.")
    print("📖 See README.md for authentication setup instructions.")
    return False


def demonstrate_basic_queries():
    """Demonstrate basic querying operations."""
    print("\n🔍 === Basic Query Operations ===")
    
    try:
        # Get all users
        print("\n1. Getting all active users...")
        active_users = User.manager.filter(is_active=True)
        print(f"   Found {active_users.size()} active users")
        
        for i, user in enumerate(active_users):
            if i >= 3:  # Limit output for demo
                print(f"   ... and {active_users.size() - 3} more")
                break
            print(f"   - {user.name} ({user.department})")
        
        # Get users by age range
        print("\n2. Getting users under 35...")
        young_users = User.manager.filter(age__lt=35)
        print(f"   Found {young_users.size()} users under 35")
        
        for user in young_users:
            print(f"   - {user.name}: {user.age} years old")
        
        # Get users by department
        print("\n3. Getting Engineering department users...")
        engineers = User.manager.filter(department="Engineering")
        print(f"   Found {engineers.size()} engineers")
        
        for user in engineers:
            print(f"   - {user.name}: {user.tags}")
        
        # Get specific user
        print("\n4. Getting specific user...")
        try:
            user = User.manager.get(name="John Doe")
            print(f"   Found: {user.name}")
            print(f"   Email: {user.email}")
            print(f"   Department: {user.department}")
            print(f"   Join Date: {user.join_date}")
            print(f"   Tags: {user.tags}")
        except ModelItemException:
            print("   User 'John Doe' not found")
        
    except Exception as e:
        print(f"❌ Error during queries: {e}")


def demonstrate_advanced_queries():
    """Demonstrate advanced querying and filtering."""
    print("\n🔧 === Advanced Query Operations ===")
    
    try:
        # Combined filters
        print("\n1. Combined filters - Active engineers...")
        active_engineers = User.manager.filter(is_active=True, department="Engineering")
        print(f"   Found {active_engineers.size()} active engineers")
        
        # Name contains filter
        print("\n2. Name contains filter - Names with 'John'...")
        johns = User.manager.filter(name__ct="John")
        print(f"   Found {johns.size()} users with 'John' in name")
        
        # Age range filters
        print("\n3. Age range filters - Users between 25-35...")
        mid_career = User.manager.filter(age__gte=25)
        print(f"   Users 25 and older: {mid_career.size()}")
        
        # Iterator operations
        print("\n4. Iterator operations...")
        all_users = User.manager.filter(is_active=True)
        if all_users.size() > 0:
            print(f"   First user: {all_users.first().name}")
            print(f"   Last user: {all_users.last().name}")
            if all_users.size() > 2:
                print(f"   Third user: {all_users.nth(2).name}")
        
    except Exception as e:
        print(f"❌ Error during advanced queries: {e}")


def demonstrate_data_validation():
    """Demonstrate data validation and error handling."""
    print("\n⚠️ === Data Validation & Error Handling ===")
    
    try:
        # Get all users and check for errors
        all_users = User.manager.filter(is_active=True)
        
        print(f"\n1. Checking data validation for {all_users.size()} users...")
        users_with_errors = []
        
        for user in all_users:
            errors = user.get_errors()
            if errors:
                users_with_errors.append((user.name, errors))
        
        if users_with_errors:
            print(f"   Found {len(users_with_errors)} users with validation errors:")
            for name, errors in users_with_errors:
                print(f"   - {name}: {errors}")
        else:
            print("   ✅ All users have valid data")
        
        # Demonstrate raw data access
        print("\n2. Raw data access...")
        if all_users.size() > 0:
            first_user = all_users.first()
            print(f"   User: {first_user.name}")
            print(f"   Raw data: {first_user.get_raw_data()}")
            print(f"   Raw name value: {first_user.get_raw_value('name')}")
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")


def demonstrate_json_serialization():
    """Demonstrate JSON serialization of model data."""
    print("\n📄 === JSON Serialization ===")
    
    try:
        # Get a few users and serialize to JSON
        users = User.manager.filter(is_active=True)
        
        print(f"\n1. Serializing {min(3, users.size())} users to JSON...")
        
        for i, user in enumerate(users):
            if i >= 3:
                break
            
            json_data = user.to_json()
            print(f"\n   User {i+1}: {user.name}")
            print(f"   JSON: {json_data}")
        
    except Exception as e:
        print(f"❌ Error during serialization: {e}")


def demonstrate_model_operations():
    """Demonstrate various model operations."""
    print("\n🔄 === Model Operations ===")
    
    try:
        # Model reloading
        print("\n1. Reloading model data...")
        User.manager.reload_model()
        print("   ✅ Model data reloaded")
        
        # Manual initialization (for lazy models)
        print("\n2. Manual model initialization...")
        User.manager.initialise_model()
        print("   ✅ Model initialized")
        
        # Get model statistics
        all_users = User.manager.filter(is_active=True)
        inactive_users = User.manager.filter(is_active=False)
        
        print(f"\n3. Model statistics:")
        print(f"   Active users: {all_users.size()}")
        print(f"   Inactive users: {inactive_users.size()}")
        print(f"   Total users: {all_users.size() + inactive_users.size()}")
        
        # Department breakdown
        departments = {}
        for user in User.manager.filter(is_active=True):
            dept = user.department
            departments[dept] = departments.get(dept, 0) + 1
        
        print(f"\n4. Department breakdown:")
        for dept, count in departments.items():
            print(f"   {dept}: {count} users")
        
    except Exception as e:
        print(f"❌ Error during model operations: {e}")


def main():
    """Main function to run the user management example."""
    print("🚀 SheetAlchemy User Management Example")
    print("=" * 50)
    
    # Step 1: Setup authentication
    if not setup_authentication():
        print("Please set up authentication to continue.")
        print("1. Create a Google Cloud Project")
        print("2. Enable Google Sheets API")
        print("3. Create service account and download key")
        print("4. Set GODM_AUTH_KEY_PATH environment variable")
        return
    
    # Step 2: Initialize the model (will connect to Google Sheets)
    print("\n📊 Initializing User model...")
    try:
        User.manager.initialise_model()
        print("✅ Connected to Google Sheets successfully!")
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        print("Please check:")
        print("- Sheet name: 'User Management Demo'")
        print("- Tab name: 'Users'")
        print("- Service account has access to the sheet")
        print("- Headers are in row 1")
        return
    
    # Step 3: Run demonstrations
    try:
        demonstrate_basic_queries()
        demonstrate_advanced_queries()
        demonstrate_data_validation()
        demonstrate_json_serialization()
        demonstrate_model_operations()
        
        print("\n🎉 Example completed successfully!")
        print("\n📚 Next steps:")
        print("- Try modifying the queries")
        print("- Add more data to your Google Sheet")
        print("- Experiment with different field types")
        print("- Check out the advanced inventory example")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your Google Sheets setup and try again")


if __name__ == "__main__":
    main()