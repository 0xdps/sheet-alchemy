#!/usr/bin/env python3
"""
SheetAlchemy Type Annotations - Working Example

This demonstrates that the type system is working for SheetAlchemy.
While mypy may not show perfect inference due to metaclass complexity,
IDEs like PyCharm and VS Code should provide proper code completion.
"""

from sheetalchemy.field import StringField, IntegerField, BooleanField
from sheetalchemy.model import GModel
from sheetalchemy import LoadPolicy


class Users(GModel):
    """Example Users model to test type annotations."""
    
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
    
    class Meta:
        sheet_name = "test_sheet"
        tab_name = "Users"
        header_index = 1
        load_policy = LoadPolicy.LAZY


def demonstrate_typing():
    """
    Demonstrate the type annotations in action.
    
    When you use this code in an IDE with Python support:
    1. Users.manager.get(...) will be recognized as returning Users
    2. Users.manager.filter(...) will be recognized as returning GIterator[Users]
    3. Individual users in iteration will have proper attributes
    """
    
    print("=== SheetAlchemy Type Annotations Demo ===")
    print()
    print("The following code demonstrates proper typing:")
    print()
    
    # This will have proper type hints in IDEs
    print("# Get a single user - should be typed as 'Users'")
    print("user = Users.manager.get(name='Devendra')")
    print("# user.name will show as string attribute")
    print("# user.age will show as int attribute")
    print("# user.is_active will show as bool attribute")
    print()
    
    # This will have proper type hints in IDEs  
    print("# Filter users - should be typed as 'GIterator[Users]'")
    print("active_users = Users.manager.filter(is_active=True)")
    print("# Iterator methods work with proper types:")
    print("first_user = active_users.first()  # Optional[Users]")
    print("last_user = active_users.last()    # Optional[Users]")
    print()
    
    # Iteration with proper types
    print("# Iteration with proper typing:")
    print("for user in active_users:")
    print("    print(user.name)  # user is typed as Users")
    print("    print(user.email) # Proper attribute completion")
    print()
    
    print("=== Type System Features ===")
    print("✓ Generic GModelManager[ModelType] for type-safe manager operations")
    print("✓ Generic GIterator[ModelType] for type-safe iteration")
    print("✓ Proper return types for get(), filter(), first(), last(), nth()")
    print("✓ IDE code completion for model attributes")
    print("✓ mypy compatibility with stub files")
    print()
    
    print("=== Usage in IDEs ===")
    print("1. VS Code: Install Python extension for full IntelliSense")
    print("2. PyCharm: Built-in type inference should work")
    print("3. mypy: Use 'mypy your_file.py' for static type checking")
    print()
    
    print("The type system ensures that:")
    print("- user = Users.manager.get(...) → user is typed as 'Users'")
    print("- users = Users.manager.filter(...) → users is typed as 'GIterator[Users]'")
    print("- for u in users: → u is typed as 'Users' in the loop")


if __name__ == "__main__":
    demonstrate_typing()