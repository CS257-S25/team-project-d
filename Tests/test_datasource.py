'''tests for datasource.py'''
import unittest
from unittest.mock import MagicMock, patch
from ProductionCode.datasource import DataSource

class TestDataSource(unittest.TestCase):
    '''class for tests for datasource.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_id_from_name")
    def test_get_activity_list_error(self, mock_get_id_from_name):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        # self.mock_conn.cursor.return_value.fetchall.return_value = ["testingggg????"]
        mock_get_id_from_name.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = None
        not_found = DataSource.get_activity_list("invalid_subcategory")
        self.assertEqual(not_found, None)

        