'''tests for datasource.py'''
import unittest
from unittest.mock import MagicMock, patch
from ProductionCode.datasource import datasource

class TestDataSource(unittest.TestCase):
    '''class for tests for datasource.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.datasource = datasource.test_client()

    def test_get_activity_list_error(self):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        self.mock_conn.cursor.return_value.fetchall.return_value = ["testingggg????"]
        not_found = datasource.get_subcategory_list("invalid_subcategory")
        self.assertEqual(not_found, None)

        