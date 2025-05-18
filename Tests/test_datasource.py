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
    # @patch("ProductionCode.datasource.get_id_from_name")
    def test_get_activity_list_error(self, mock_connect):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        # mock_get_id_from_name.return_value = None
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        not_found = ds.get_activity_list("invalid_subcategory")
        self.assertEqual(not_found, None)
        self.mock_cursor.execute.assert_not_called()

        