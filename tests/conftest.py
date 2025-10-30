# Test Configuration and Fixtures for G-ODM

import pytest
from unittest.mock import Mock, MagicMock, patch
import gspread
from godm.field import StringField, IntegerField, DateField, BooleanField, ListField, CustomField
from godm.model import GModel
from godm import LoadPolicy


@pytest.fixture
def mock_worksheet():
    """Create a mock worksheet with sample data."""
    worksheet = Mock(spec=gspread.Worksheet)
    
    # Mock header row
    worksheet.row_values.return_value = ["Name", "Age", "Email", "Active", "Tags", "DOB"]
    
    # Mock data rows
    def mock_row_values(row_num):
        sample_data = {
            1: ["Name", "Age", "Email", "Active", "Tags", "DOB"],  # Header
            2: ["John Doe", "25", "john@example.com", "true", "developer,python", "01/15/1999"],
            3: ["Jane Smith", "30", "jane@example.com", "false", "designer,ui", "05/20/1994"],
            4: ["Bob Wilson", "35", "bob@example.com", "true", "manager", "12/10/1989"],
        }
        return sample_data.get(row_num, [])
    
    def mock_col_values(col_num):
        """Mock column values for filtering."""
        sample_columns = {
            1: ["Name", "John Doe", "Jane Smith", "Bob Wilson"],      # Name column
            2: ["Age", "25", "30", "35"],                             # Age column  
            3: ["Email", "john@example.com", "jane@example.com", "bob@example.com"],
            4: ["Active", "true", "false", "true"],                   # Active column
            5: ["Tags", "developer,python", "designer,ui", "manager"],
            6: ["DOB", "01/15/1999", "05/20/1994", "12/10/1989"],
        }
        return sample_columns.get(col_num, [])
    
    worksheet.row_values.side_effect = mock_row_values
    worksheet.col_values.side_effect = mock_col_values
    
    return worksheet


@pytest.fixture
def mock_spreadsheet(mock_worksheet):
    """Create a mock spreadsheet."""
    spreadsheet = Mock(spec=gspread.Spreadsheet)
    spreadsheet.worksheet.return_value = mock_worksheet
    return spreadsheet


@pytest.fixture
def mock_gspread_client(mock_spreadsheet):
    """Create a mock gspread client."""
    client = Mock(spec=gspread.Client)
    client.open.return_value = mock_spreadsheet
    return client


@pytest.fixture(autouse=True)
def mock_auth(mock_gspread_client):
    """Auto-mock authentication for all tests."""
    with patch('godm._auth._g_sheet', mock_gspread_client):
        with patch('godm._auth.get_sheet') as mock_get_sheet:
            mock_get_sheet.return_value = mock_gspread_client.open()
            yield mock_get_sheet


class SampleUserModel(GModel):
    """Sample model for testing."""
    name = StringField(name="Name")
    age = IntegerField(name="Age")
    email = StringField(name="Email", allow_empty_or_null=True)
    is_active = BooleanField(name="Active")
    tags = ListField(name="Tags", delimiter=",", item_type=str)
    dob = DateField(name="DOB", format=DateField.MM_DD_YYYY, allow_empty_or_null=True)
    
    class Meta:
        sheet_name = "Test Sheet"
        tab_name = "Users"
        header_index = 1
        load_policy = LoadPolicy.LAZY


@pytest.fixture
def sample_user_model():
    """Provide the sample user model for testing."""
    return SampleUserModel


@pytest.fixture
def sample_field_data():
    """Sample field data for testing."""
    return {
        "Name": "Test User",
        "Age": "25",
        "Email": "test@example.com",
        "Active": "true",
        "Tags": "developer,python,testing",
        "DOB": "01/15/1999",
        "Name_transform": "Test User",
        "Age_transform": "25",
        "Email_transform": "test@example.com",
        "Active_transform": "true", 
        "Tags_transform": "developer,python,testing",
        "DOB_transform": "01/15/1999",
    }


# Test data constants
VALID_EMAIL = "test@example.com"
VALID_DATE_MM_DD_YYYY = "01/15/1999"
VALID_DATE_DD_MM_YYYY = "15/01/1999"
INVALID_DATE = "not-a-date"
VALID_TAG_LIST = "python,django,web"
VALID_BOOLEAN_TRUE = ["true", "True", "TRUE", "yes", "y", "1", "ok"]
VALID_BOOLEAN_FALSE = ["false", "False", "FALSE", "no", "n", "0"]