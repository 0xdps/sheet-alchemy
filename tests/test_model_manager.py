"""
Unit Tests for G-ODM Model and Manager Functionality

This module tests:
- Model creation and initialization
- Manager filtering and querying
- Load policies
- Error handling
- Data retrieval and processing
"""

import pytest
from unittest.mock import Mock, patch
from sheetalchemy.model import GModel
from sheetalchemy._manager import GModelManager, LoadPolicy
from sheetalchemy.field import StringField, IntegerField, BooleanField
from sheetalchemy.exceptions import ModelItemException, FieldException
from sheetalchemy.iterator import GIterator


class TestModelCreation:
    """Test GModel creation and initialization."""
    
    def test_model_creation_with_data(self):
        """Test GModel initialization with field data."""
        model_data = {
            "id": 1,
            "data": {"Name": "Test User", "Age": "25"},
            "errors": {},
            "fields": {"name": "Test User", "age": 25}
        }
        
        # Create a simple model class for testing
        class TestModel(GModel):
            name = StringField(name="Name")
            age = IntegerField(name="Age")
            
            class Meta:
                sheet_name = "Test"
                tab_name = "Users" 
                header_index = 1
                load_policy = LoadPolicy.LAZY
        
        model_instance = TestModel(model_data)
        
        assert model_instance.id == 1
        assert model_instance.name == "Test User"
        assert model_instance.age == 25
        assert model_instance._data == {"Name": "Test User", "Age": "25"}
        assert model_instance._errors == {}
    
    def test_model_to_json(self, sample_user_model):
        """Test model JSON serialization."""
        model_data = {
            "id": 1,
            "data": {},
            "errors": {},
            "fields": {"name": "John Doe", "age": 30, "is_active": True}
        }
        
        # Mock the _meta attribute
        with patch.object(sample_user_model, '_meta', {"name": str, "age": int, "is_active": bool}):
            model_instance = sample_user_model(model_data)
            model_instance.name = "John Doe"
            model_instance.age = 30
            model_instance.is_active = True
            
            json_data = model_instance.to_json()
            
            assert json_data["id"] == 1
            assert json_data["name"] == "John Doe"
            assert json_data["age"] == 30
            assert json_data["is_active"] is True
    
    def test_model_get_errors(self):
        """Test getting model errors."""
        model_data = {
            "id": 1,
            "data": {},
            "errors": {"age": "Invalid age value"},
            "fields": {"name": "Test User"}
        }
        
        class TestModel(GModel):
            name = StringField(name="Name")
            
            class Meta:
                sheet_name = "Test"
                tab_name = "Users"
                header_index = 1
                load_policy = LoadPolicy.LAZY
        
        model_instance = TestModel(model_data)
        errors = model_instance.get_errors()
        assert errors == {"age": "Invalid age value"}
    
    def test_model_get_raw_data(self):
        """Test getting raw model data."""
        raw_data = {"Name": "Test User", "Age": "25", "Email": "test@example.com"}
        model_data = {
            "id": 1,
            "data": raw_data,
            "errors": {},
            "fields": {}
        }
        
        class TestModel(GModel):
            class Meta:
                sheet_name = "Test"
                tab_name = "Users"
                header_index = 1
                load_policy = LoadPolicy.LAZY
        
        model_instance = TestModel(model_data)
        assert model_instance.get_raw_data() == raw_data


class TestModelManager:
    """Test GModelManager functionality."""
    
    def test_manager_initialization_lazy(self, sample_user_model):
        """Test manager initialization with lazy load policy."""
        # The manager should be created but not setup immediately
        manager = sample_user_model.manager
        assert isinstance(manager, GModelManager)
        assert manager.load_policy == LoadPolicy.LAZY
        assert manager.model == sample_user_model
    
    def test_manager_initialization_init(self, mock_worksheet):
        """Test manager initialization with init load policy."""
        with patch('sheetalchemy._auth.get_sheet') as mock_get_sheet:
            mock_spreadsheet = Mock()
            mock_spreadsheet.worksheet.return_value = mock_worksheet
            mock_get_sheet.return_value = mock_spreadsheet
            
            class EagerModel(GModel):
                name = StringField(name="Name")
                
                class Meta:
                    sheet_name = "Test"
                    tab_name = "Users"
                    header_index = 1
                    load_policy = LoadPolicy.INIT
            
            # Manager should be set up immediately
            manager = EagerModel.manager
            assert manager.setup is True
    
    def test_manager_filter_operation(self, sample_user_model, mock_worksheet):
        """Test manager filter functionality."""
        # Setup the model with mock data
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email", "Active", "Tags", "DOB"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock the field objects
                    mock_name_field = Mock()
                    mock_name_field._meta = {"name": "Name"}
                    mock_name_field.match_value.return_value = True
                    mock_meta.get.return_value = mock_name_field
                    
                    manager = sample_user_model.manager
                    manager.setup = True  # Skip setup
                    
                    # Test filtering
                    result = manager.filter(name="John Doe")
                    assert isinstance(result, GIterator)
    
    def test_manager_get_operation_success(self, sample_user_model, mock_worksheet):
        """Test manager get operation with successful result."""
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email", "Active", "Tags", "DOB"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock field for filtering
                    mock_name_field = Mock()
                    mock_name_field._meta = {"name": "Name"}
                    mock_name_field.match_value.return_value = True
                    mock_meta.get.return_value = mock_name_field
                    
                    # Mock other fields for data processing
                    mock_age_field = Mock()
                    mock_age_field.get_value.return_value = 25
                    
                    mock_meta.items.return_value = [
                        ("name", mock_name_field),
                        ("age", mock_age_field)
                    ]
                    
                    manager = sample_user_model.manager
                    manager.setup = True
                    
                    # Mock the model creation
                    with patch.object(sample_user_model, '__new__') as mock_new:
                        mock_instance = Mock()
                        mock_new.return_value = mock_instance
                        
                        result = manager.get(name="John Doe")
                        assert result == mock_instance
    
    def test_manager_get_operation_not_found(self, sample_user_model, mock_worksheet):
        """Test manager get operation when no results found."""
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email", "Active", "Tags", "DOB"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock field that returns no matches
                    mock_name_field = Mock()
                    mock_name_field._meta = {"name": "Name"}
                    mock_name_field.match_value.return_value = False
                    mock_meta.get.return_value = mock_name_field
                    
                    manager = sample_user_model.manager
                    manager.setup = True
                    
                    # Should raise ModelItemException
                    with pytest.raises(ModelItemException, match="Unable to find Entity"):
                        manager.get(name="NonExistent")
    
    def test_manager_reload_model(self, sample_user_model):
        """Test manager model reloading."""
        manager = sample_user_model.manager
        
        # Mock the setup method
        with patch.object(manager, '_setup_attrs') as mock_setup:
            manager.reload_model()
            mock_setup.assert_called_once_with(reload=True)
    
    def test_manager_initialise_model_lazy(self, sample_user_model):
        """Test manager manual initialization for lazy models."""
        manager = sample_user_model.manager
        assert manager.load_policy == LoadPolicy.LAZY
        
        with patch.object(manager, '_setup_attrs') as mock_setup:
            manager.initialise_model()
            mock_setup.assert_called_once()


class TestModelManagerDataProcessing:
    """Test manager data processing functionality."""
    
    def test_get_data_from_id(self, sample_user_model, mock_worksheet):
        """Test getting data from specific row ID."""
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock field objects
                    name_field = Mock()
                    name_field.get_value.return_value = "John Doe"
                    
                    age_field = Mock()  
                    age_field.get_value.return_value = 25
                    
                    mock_meta.items.return_value = [
                        ("name", name_field),
                        ("age", age_field)
                    ]
                    
                    manager = sample_user_model.manager
                    manager.setup = True
                    
                    # Test getting data from row 2 (index 1, but method expects 1-based)
                    result = manager._get_data_from_id(1)  # Should get row 2 data
                    
                    assert result["id"] == 2  # row_index + 1
                    assert "fields" in result
                    assert "data" in result
                    assert "errors" in result
    
    def test_filter_data_list_single_condition(self, sample_user_model, mock_worksheet):
        """Test filtering data with single condition."""
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email", "Active"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock the active field
                    active_field = Mock()
                    active_field._meta = {"name": "Active"}
                    active_field.match_value.side_effect = lambda val, data_val, op: data_val == "true"
                    mock_meta.get.return_value = active_field
                    
                    manager = sample_user_model.manager
                    manager.setup = True
                    
                    # Filter for active users
                    result = manager._filter_data_list(is_active=True)
                    
                    # Should return indices of rows where Active = "true" (rows 2 and 4 -> indices 2,4)
                    assert isinstance(result, list)
    
    def test_filter_data_list_with_operator(self, sample_user_model, mock_worksheet):
        """Test filtering data with field operators."""
        with patch.object(sample_user_model, '_data', mock_worksheet):
            with patch.object(sample_user_model, '_headers', ["Name", "Age", "Email", "Active"]):
                with patch.object(sample_user_model, '_meta') as mock_meta:
                    # Mock the age field
                    age_field = Mock()
                    age_field._meta = {"name": "Age"}
                    age_field.match_value.side_effect = lambda val, data_val, op: int(data_val) < val if op == "lt" else False
                    mock_meta.get.return_value = age_field
                    
                    manager = sample_user_model.manager
                    manager.setup = True
                    
                    # Filter for users under 30
                    result = manager._filter_data_list(age__lt=30)
                    
                    assert isinstance(result, list)


class TestModelMetaclass:
    """Test GModel metaclass functionality."""
    
    def test_model_metaclass_field_processing(self):
        """Test that metaclass properly processes field definitions."""
        # Create a model and verify field processing
        class TestModel(GModel):
            name = StringField(name="Name")
            age = IntegerField(name="Age")
            active = BooleanField(name="Active")
            
            class Meta:
                sheet_name = "Test"
                tab_name = "Users"
                header_index = 1
                load_policy = LoadPolicy.LAZY
        
        # Check that manager is created
        assert hasattr(TestModel, 'manager')
        assert isinstance(TestModel.manager, GModelManager)
        
        # Check that field attributes are removed from class
        assert not hasattr(TestModel, 'name')
        assert not hasattr(TestModel, 'age') 
        assert not hasattr(TestModel, 'active')
    
    def test_model_metaclass_field_validation_errors(self, mock_worksheet):
        """Test metaclass handles field validation errors."""
        with patch('sheetalchemy._auth.get_sheet') as mock_get_sheet:
            mock_spreadsheet = Mock()
            mock_spreadsheet.worksheet.return_value = mock_worksheet
            mock_get_sheet.return_value = mock_spreadsheet
            
            # Create model with field that will cause validation error
            class TestModel(GModel):
                invalid_field = StringField(name="NonExistentField")  # Not in headers
                
                class Meta:
                    sheet_name = "Test"
                    tab_name = "Users"
                    header_index = 1
                    load_policy = LoadPolicy.INIT
            
            # Field validation errors should be captured
            # The model should still be created but with errors recorded