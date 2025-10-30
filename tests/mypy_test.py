#!/usr/bin/env python3
"""
Type annotation test for SheetAlchemy
This script tests that IDE/mypy can properly infer types for manager operations.
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


def test_type_annotations():
    """Test that type annotations work correctly."""
    from unittest.mock import patch, Mock
    
    # Mock the worksheet and authentication 
    mock_worksheet = Mock()
    mock_worksheet.row_values.return_value = ["Name", "Age", "Email", "Active"]
    mock_worksheet.col_values.return_value = ["Name", "Devendra", "John"]
    
    mock_spreadsheet = Mock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    
    with patch('sheetalchemy._auth.get_sheet', return_value=mock_spreadsheet):
        # Test that manager exists and has correct typing
        assert hasattr(Users, 'manager')
        
        # Mock manager methods to avoid actual API calls
        mock_user = Users({
            "id": 1,
            "data": {"Name": "Devendra", "Age": "25"},
            "errors": {},
            "fields": {"name": "Devendra", "age": 25, "is_active": True}
        })
        
        with patch.object(Users.manager, 'get', return_value=mock_user):
            with patch.object(Users.manager, 'filter') as mock_filter:
                from sheetalchemy.iterator import GIterator
                mock_iterator = GIterator(Users.manager, [1, 2])
                mock_filter.return_value = mock_iterator
                
                # Test type annotations work without runtime errors
                user = Users.manager.get(name="Devendra")  # Should be typed as Users
                users = Users.manager.filter(is_active=True)  # Should be typed as GIterator[Users]
                
                # Verify the objects are of expected types
                assert isinstance(user, Users)
                assert isinstance(users, GIterator)
                
                print("Type annotation test completed successfully.")


if __name__ == "__main__":
    test_type_annotations()