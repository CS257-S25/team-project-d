'''tests for datasource.py'''
import unittest
import psycopg2
from unittest.mock import MagicMock, patch
from ProductionCode.datasource import DataSource

class TestDataSource(unittest.TestCase):
    '''class for tests for datasource.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_id_from_name")
    def test_get_activity_list(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        mock_get_id_from_name.return_value = (["Sleeping", "Sleeplessness"])
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        not_found = ds.get_activity_list(["Sleeping", "Sleeplessness"])
        print(f"not_found: {not_found}")
        self.assertEqual(not_found, ["Sleeping", "Sleeplessness"])

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_id_from_name")
    def test_get_activity_list_error(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        mock_get_id_from_name.return_value = None
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        not_found = ds.get_activity_list("invalid_subcategory")
        self.assertEqual(not_found, None)
        self.mock_cursor.execute.assert_not_called()

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_id_from_name")
    def test_get_subcategory_list_error(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for get_subcategory_list when category is not found'''
        mock_get_id_from_name.return_value = None
        mock_connect.return_value = self.mock_conn
        ds = DataSource()
        not_found = ds.get_subcategory_list("invalid_category")
        self.assertEqual(not_found, None)
        self.mock_cursor.execute.assert_not_called()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_correct_list_error(self, mock_connect):
        '''tests the error is returned from get_correct_list when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.side_effect = psycopg2.Error()
        ds = DataSource()
        result = ds.get_correct_list("test", "SELECT")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_id_from_name_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSource()
        result = ds.get_id_from_name("test_table", "test_id", "test_column", "test_name")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_name_from_id(self, mock_connect):
        '''tests the name is returned from get_id_from_name when given id'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = ([["Personal_Care_Activities",],])
        ds = DataSource()
        result = ds.get_name_from_id("category", "Category_ID", "Category_Name", "T01")
        self.assertEqual(result, "Personal_Care_Activities")
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_name_from_id_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSource()
        result = ds.get_name_from_id("test_table", "test_col_id", "test_column", "test_id")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_id_from_name")
    @patch("ProductionCode.datasource.DataSource.get_name_from_id")
    def test_get_subcategory_from_activity(self, mock_get_name_from_id, mock_get_id_from_name, mock_connect):
        '''tests the subcategory is returned from get_subcategory_from_activity when activity'''
        mock_connect.return_value = self.mock_conn
        mock_connect.cursor.return_value = self.mock_cursor
        mock_get_id_from_name.return_value = "T0101"
        mock_get_name_from_id.return_value = "Sleeping"
        ds = DataSource()
        result = ds.get_subcategory_from_activity("Sleeplessness")
        self.assertEqual(result, "Sleeping")

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_subcategory_from_activity_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSource()
        result = ds.get_subcategory_from_activity("test_activity")
        self.assertEqual(result, None)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_top_records_error(self, mock_connect):
        '''tests the error is returned from get_top_records when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSource()
        result = ds.get_top_records("test_activities")
        self.assertEqual(result, None)