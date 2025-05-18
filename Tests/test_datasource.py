'''tests for datasource.py'''
import unittest
from unittest.mock import MagicMock, patch
from ProductionCode.datasource import DataSource
from ProductionCode.datasource import get_activity_list

class TestDataSource(unittest.TestCase):
    '''class for tests for datasource.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_activity_list_error(self, mock_get_activity_list):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        # self.mock_conn.cursor.return_value.fetchall.return_value = ["testingggg????"]
        mock_get_activity_list.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = None
        not_found = get_activity_list("invalid_subcategory")
        self.assertEqual(not_found, None)

        