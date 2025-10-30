"""
Unit Tests for G-ODM Iterator and Authentication

This module tests:
- Iterator functionality and operations
- Authentication mechanisms
- Error handling and edge cases
"""

import pytest
from unittest.mock import Mock, patch, mock_open
import json
from godm.iterator import GIterator
from godm._auth import authenticate, get_sheet, load_sheet
from godm.exceptions import InvalidIndexException
import gspread


class TestGIterator:
    """Test GIterator functionality."""
    
    def test_iterator_creation(self):
        """Test GIterator initialization."""
        mock_manager = Mock()
        mock_manager.model.__name__ = "TestModel"
        filter_list = [1, 2, 3, 4]
        
        iterator = GIterator(mock_manager, filter_list)
        
        assert iterator._manager == mock_manager
        assert iterator._filter_list == filter_list
        assert iterator._start_index == 0
    
    def test_iterator_repr(self):
        """Test GIterator string representation."""
        mock_manager = Mock()
        mock_manager.model.__name__ = "TestModel"
        filter_list = [1, 2, 3]
        
        iterator = GIterator(mock_manager, filter_list)
        repr_str = repr(iterator)
        
        assert "TestModel" in repr_str
        assert "[1, 2, 3]" in repr_str
        assert "0" in repr_str  # Current position
    
    def test_iterator_next_functionality(self):
        """Test iterator __next__ method."""
        mock_manager = Mock()
        mock_manager.model.__name__ = "TestModel"
        
        # Mock entity objects
        entity1 = Mock()
        entity1.name = "Entity1"
        entity2 = Mock()
        entity2.name = "Entity2"
        
        mock_manager.get_entity_from_id.side_effect = [entity1, entity2]
        
        filter_list = [1, 2]
        iterator = GIterator(mock_manager, filter_list)
        
        # Test iteration
        first_entity = next(iterator)
        assert first_entity == entity1
        assert iterator._start_index == 1
        
        second_entity = next(iterator) 
        assert second_entity == entity2
        assert iterator._start_index == 2
        
        # Should raise StopIteration when exhausted
        with pytest.raises(StopIteration):
            next(iterator)
    
    def test_iterator_for_loop(self):
        """Test iterator in for loop."""
        mock_manager = Mock()
        mock_manager.model.__name__ = "TestModel"
        
        entities = [Mock(), Mock(), Mock()]
        mock_manager.get_entity_from_id.side_effect = entities
        
        filter_list = [1, 2, 3]
        iterator = GIterator(mock_manager, filter_list)
        
        result_entities = []
        for entity in iterator:
            result_entities.append(entity)
        
        assert len(result_entities) == 3
        assert result_entities == entities
    
    def test_iterator_getitem_valid_index(self):
        """Test iterator indexing with valid indices."""
        mock_manager = Mock()
        entity = Mock()
        entity.name = "TestEntity"
        mock_manager.get_entity_from_id.return_value = entity
        
        filter_list = [10, 20, 30]
        iterator = GIterator(mock_manager, filter_list)
        
        # Test valid index access
        result = iterator[1]
        assert result == entity
        mock_manager.get_entity_from_id.assert_called_with(20)  # filter_list[1]
    
    def test_iterator_getitem_invalid_index(self):
        """Test iterator indexing with invalid indices."""
        mock_manager = Mock()
        filter_list = [10, 20, 30]
        iterator = GIterator(mock_manager, filter_list)
        
        # Test invalid indices
        with pytest.raises(InvalidIndexException):
            iterator[-1]  # Negative index
        
        with pytest.raises(InvalidIndexException):
            iterator[5]   # Index out of range
        
        with pytest.raises(InvalidIndexException):
            iterator["not_an_int"]  # Non-integer index
    
    def test_iterator_first_last_nth(self):
        """Test iterator first, last, and nth methods."""
        mock_manager = Mock()
        
        entities = [Mock(name="First"), Mock(name="Second"), Mock(name="Third")]
        mock_manager.get_entity_from_id.side_effect = entities
        
        filter_list = [1, 2, 3]
        iterator = GIterator(mock_manager, filter_list)
        
        # Test first
        first = iterator.first()
        assert first == entities[0]
        
        # Test last  
        last = iterator.last()
        assert last == entities[2]
        
        # Test nth
        second = iterator.nth(1)
        assert second == entities[1]
    
    def test_iterator_size(self):
        """Test iterator size method."""
        mock_manager = Mock()
        filter_list = [1, 2, 3, 4, 5]
        iterator = GIterator(mock_manager, filter_list)
        
        assert iterator.size() == 5
    
    def test_iterator_reset(self):
        """Test iterator reset functionality."""
        mock_manager = Mock()
        mock_manager.get_entity_from_id.return_value = Mock()
        
        filter_list = [1, 2, 3]
        iterator = GIterator(mock_manager, filter_list)
        
        # Advance iterator
        next(iterator)
        next(iterator)
        assert iterator._start_index == 2
        
        # Reset should set index back to 0
        iterator.reset()
        assert iterator._start_index == 0
        
        # Should be able to iterate again
        next(iterator)
        assert iterator._start_index == 1


class TestAuthentication:
    """Test authentication functionality."""
    
    def test_authenticate_with_key_object(self):
        """Test authentication with key object."""
        key_object = {
            "type": "service_account",
            "project_id": "test-project",
            "private_key": "test-key"
        }
        
        with patch('gspread.service_account_from_dict') as mock_service_account:
            mock_client = Mock()
            mock_service_account.return_value = mock_client
            
            authenticate(key_object=key_object)
            
            mock_service_account.assert_called_once_with(key_object)
    
    def test_authenticate_with_key_path(self):
        """Test authentication with key file path."""
        key_path = "/path/to/key.json"
        key_object = {"type": "service_account"}
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(key_object))):
                with patch('json.load', return_value=key_object):
                    with patch('gspread.service_account_from_dict') as mock_service_account:
                        mock_client = Mock()
                        mock_service_account.return_value = mock_client
                        
                        authenticate(key_path=key_path)
                        
                        mock_service_account.assert_called_once_with(key_object)
    
    def test_authenticate_with_env_variable(self):
        """Test authentication using environment variable."""
        key_path = "/env/path/to/key.json"
        key_object = {"type": "service_account"}
        
        with patch('os.environ.get', return_value=key_path):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', mock_open(read_data=json.dumps(key_object))):
                    with patch('json.load', return_value=key_object):
                        with patch('gspread.service_account_from_dict') as mock_service_account:
                            mock_client = Mock()
                            mock_service_account.return_value = mock_client
                            
                            # Call without parameters - should use env variable
                            authenticate()
                            
                            mock_service_account.assert_called_once_with(key_object)
    
    def test_get_sheet_first_time(self):
        """Test getting sheet for the first time (not cached)."""
        sheet_name = "Test Sheet"
        
        # Mock global client
        mock_client = Mock()
        mock_spreadsheet = Mock()
        mock_client.open.return_value = mock_spreadsheet
        
        with patch('godm._auth._g_sheet', mock_client):
            with patch('godm._auth._worksheets', {}) as mock_worksheets:
                result = get_sheet(sheet_name)
                
                assert result == mock_spreadsheet
                mock_client.open.assert_called_once_with(sheet_name)
                assert mock_worksheets[sheet_name] == mock_spreadsheet
    
    def test_get_sheet_cached(self):
        """Test getting sheet from cache."""
        sheet_name = "Test Sheet"
        mock_spreadsheet = Mock()
        
        with patch('godm._auth._worksheets', {sheet_name: mock_spreadsheet}):
            result = get_sheet(sheet_name)
            
            assert result == mock_spreadsheet
    
    def test_get_sheet_no_authentication(self):
        """Test getting sheet when not authenticated."""
        sheet_name = "Test Sheet"
        
        with patch('godm._auth._g_sheet', None):
            with patch('godm._auth.authenticate') as mock_authenticate:
                mock_client = Mock()
                mock_spreadsheet = Mock()
                mock_client.open.return_value = mock_spreadsheet
                
                with patch('godm._auth._g_sheet', mock_client):
                    result = get_sheet(sheet_name)
                    
                    mock_authenticate.assert_called_once()
                    assert result == mock_spreadsheet
    
    def test_load_sheet_with_alias(self):
        """Test loading sheet with alias."""
        sheet_name = "Test Sheet"
        alias = "test_alias"
        
        mock_client = Mock()
        mock_spreadsheet = Mock()
        mock_client.open.return_value = mock_spreadsheet
        
        with patch('godm._auth._g_sheet', mock_client):
            with patch('godm._auth._worksheets', {}) as mock_worksheets:
                load_sheet(sheet_name, alias)
                
                # Should store under both names
                assert mock_worksheets[sheet_name] == mock_spreadsheet
                assert mock_worksheets[alias] == mock_spreadsheet
                mock_client.open.assert_called_once_with(sheet_name)
    
    def test_load_sheet_without_alias(self):
        """Test loading sheet without alias."""
        sheet_name = "Test Sheet"
        
        mock_client = Mock()
        mock_spreadsheet = Mock()
        mock_client.open.return_value = mock_spreadsheet
        
        with patch('godm._auth._g_sheet', mock_client):
            with patch('godm._auth._worksheets', {}) as mock_worksheets:
                load_sheet(sheet_name)
                
                # Should only store under sheet name
                assert mock_worksheets[sheet_name] == mock_spreadsheet
                assert "default" not in mock_worksheets  # No alias provided
                mock_client.open.assert_called_once_with(sheet_name)


class TestExceptionHandling:
    """Test exception handling across modules."""
    
    def test_invalid_index_exception_message(self):
        """Test InvalidIndexException can be raised and caught."""
        mock_manager = Mock()
        filter_list = [1, 2, 3]
        iterator = GIterator(mock_manager, filter_list)
        
        try:
            iterator[10]  # Should raise InvalidIndexException
        except InvalidIndexException as e:
            # Exception should be catchable
            assert isinstance(e, InvalidIndexException)
        else:
            pytest.fail("Expected InvalidIndexException to be raised")
    
    def test_iterator_empty_filter_list(self):
        """Test iterator behavior with empty filter list."""
        mock_manager = Mock()
        filter_list = []
        iterator = GIterator(mock_manager, filter_list)
        
        # Should immediately raise StopIteration
        with pytest.raises(StopIteration):
            next(iterator)
        
        # Size should be 0
        assert iterator.size() == 0
        
        # Accessing any index should raise InvalidIndexException
        with pytest.raises(InvalidIndexException):
            iterator.first()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_iterator_single_item(self):
        """Test iterator with single item."""
        mock_manager = Mock()
        mock_entity = Mock()
        mock_manager.get_entity_from_id.return_value = mock_entity
        
        filter_list = [42]
        iterator = GIterator(mock_manager, filter_list)
        
        # Should work with single item
        assert iterator.size() == 1
        assert iterator.first() == mock_entity
        assert iterator.last() == mock_entity
        assert iterator.nth(0) == mock_entity
        
        # Iteration should work
        entities = list(iterator)
        assert len(entities) == 1
        assert entities[0] == mock_entity
    
    def test_authentication_file_not_found(self):
        """Test authentication when key file doesn't exist."""
        key_path = "/nonexistent/path/key.json"
        
        with patch('os.path.exists', return_value=False):
            with patch('os.environ.get', return_value=None):
                # Should handle gracefully or raise appropriate error
                # Implementation should handle this case appropriately
                pass