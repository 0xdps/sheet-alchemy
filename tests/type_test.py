#!/usr/bin/env python3
"""
Type annotation test for SheetAlchemy
This script tests that IDE/mypy can properly infer types for manager operations.
"""

from sheetalchemy.field import StringField, IntegerField, BooleanField
from sheetalchemy.model import GModel
from sheetalchemy._manager import LoadPolicy


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


def test_type_annotations():
    """Test that type annotations work correctly."""
    
    # This should show 'user' as type 'Users' in IDEs
    # user = Users.manager.get(name="Devendra")
    
    # This should show 'users' as type 'GIterator[Users]' in IDEs  
    # users = Users.manager.filter(is_active=True)
    
    # This should show individual items as type 'Users' when iterating
    # for user in users:
    #     print(user.name)  # Should show .name as string attribute
    
    print("Type annotation test file created.")
    print("To test:")
    print("1. Open this file in an IDE with Python support")
    print("2. Uncomment the lines above")
    print("3. Check that 'user' variable shows type 'Users'")
    print("4. Check that 'users' variable shows type 'GIterator[Users]'")
    print("5. Run 'mypy type_test.py' to validate types")


if __name__ == "__main__":
    test_type_annotations()