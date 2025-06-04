'''tests for datasource.py'''
import unittest
from unittest.mock import MagicMock, patch
import psycopg2
from ProductionCode.datasource_compare import DataSource as DataSourceCompare
from ProductionCode.datasource_top import DataSource as DataSourceTop
from ProductionCode.datasource_activities import DataSource as DataSourceActivities

class TestDataSource(unittest.TestCase):
    '''class for tests for datasource.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    @patch("ProductionCode.datasource_activities.DataSource.get_names_from_list")
    @patch("ProductionCode.datasource_activities.DataSource.get_id_from_name")
    def test_get_activity_list(self, mock_get_id_from_name, mock_get_names_from_list, mock_connect):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        mock_get_id_from_name.return_value = "T0101"
        mock_get_names_from_list.return_value = ["Sleeping", "Sleeplessness"]
        mock_connect.return_value = self.mock_conn
        ds = DataSourceActivities()
        result = ds.get_activity_list("Sleeping")
        self.assertEqual(result, ["Sleeping", "Sleeplessness"])

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    @patch("ProductionCode.datasource_activities.DataSource.get_activity_list")
    def test_get_activity_list_error(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for get_activity_list when subcategory is not found'''
        mock_get_id_from_name.return_value = None
        mock_connect.return_value = self.mock_conn
        ds = DataSourceActivities()
        not_found = ds.get_activity_list("invalid_subcategory")
        self.assertEqual(not_found, None)
        self.mock_cursor.execute.assert_not_called()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    @patch("ProductionCode.datasource_activities.get_id_from_name")
    def test_get_subcategory_list_error(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for get_subcategory_list when category is not found'''
        mock_get_id_from_name.return_value = None
        mock_connect.return_value = self.mock_conn
        ds = DataSourceActivities()
        not_found = ds.get_subcategory_list("invalid_category")
        self.assertEqual(not_found, None)
        self.mock_cursor.execute.assert_not_called()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_get_correct_list_error(self, mock_connect):
        '''tests the error is returned from get_correct_list when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.side_effect = psycopg2.Error()
        ds = DataSourceActivities()
        result = ds.get_correct_list("test", "SELECT")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_get_id_from_name_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceActivities()
        result = ds.get_id_from_name("test_table", "test_id", "test_column", "test_name")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_get_name_from_id(self, mock_connect):
        '''tests the name is returned from get_id_from_name when given id'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = ([["Personal Care Activities",],])
        ds = DataSourceActivities()
        result = ds.get_name_from_id("category", "Category ID", "Category Name", "T01")
        self.assertEqual(result, "Personal Care Activities")
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_get_name_from_id_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceActivities()
        result = ds.get_name_from_id("test_table", "test_col_id", "test_column", "test_id")
        self.assertEqual(result, None)
        self.mock_cursor.execute.assert_called_once()

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    @patch("ProductionCode.datasource_activities.DataSource.get_id_from_name")
    @patch("ProductionCode.datasource_activities.DataSource.get_name_from_id")
    def test_get_subcategory_from_activity(self, mock_get_name_from_id,
                                           mock_get_id_from_name, mock_connect):
        '''tests the subcategory is returned from get_subcategory_from_activity when activity'''
        mock_connect.return_value = self.mock_conn
        mock_connect.cursor.return_value = self.mock_cursor
        mock_get_id_from_name.return_value = "T0101"
        mock_get_name_from_id.return_value = "Sleeping"
        ds = DataSourceActivities()
        result = ds.get_subcategory_from_activity("Sleeplessness")
        self.assertEqual(result, "Sleeping")

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_get_subcategory_from_activity_error(self, mock_connect):
        '''tests the error is returned from get_id_from_name when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceActivities()
        result = ds.get_subcategory_from_activity("test_activity")
        self.assertEqual(result, None)

    @patch("ProductionCode.datasource_top.psycopg2.connect")
    def test_get_top_records_error(self, mock_connect):
        '''tests the error is returned from get_top_records when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceTop()
        result = ds.get_top_records("test_activities")
        self.assertEqual(result, None)

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_compare_by_age_invalid_age(self, mock_connect):
        '''tests the invalid age message is returned from 
        get_top_records when age isn't a number'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceCompare()
        result = ds.compare_by_age("test_age", "test_activity")
        self.assertEqual(result, "invalid age, please use a number between 15 and 80")

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    def test_compare_by_age_out_of_range(self, mock_connect):
        '''tests the invalid age message is returned from 
        get_top_records when age is out of range'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceCompare()
        result = ds.compare_by_age(100, "test_activity")
        self.assertEqual(result, "invalid age, please use a number between 15 and 80")

    @patch("ProductionCode.datasource_activities.psycopg2.connect")
    @patch("ProductionCode.datasource_activities.DataSource.get_id_from_name")
    def test_compare_by_age(self, mock_get_id_from_name, mock_connect):
        '''tests the correct result for compare_by_age'''
        mock_get_id_from_name.return_value = "T010101"
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [[559], [552]]
        ds = DataSourceCompare()
        result = ds.compare_by_age(23, "Sleeping")
        self.assertEqual(result, (559, 552))
        self.mock_cursor.execute.assert_called_once()
        self.mock_cursor.fetchall.assert_called_once()

    @patch("ProductionCode.datasource_compare.psycopg2.connect")
    @patch("ProductionCode.datasource_compare.DataSource")
    def test_compare_by_age_no_data(self, mock_get_id_from_name, mock_connect):
        '''tests the correct error message for compare_by_age when no data found'''
        mock_get_id_from_name.return_value = "T010101"
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = None
        ds = DataSourceCompare()
        result = ds.compare_by_age(23, "Sleeping")
        print(f"compare by age result: {result}")
        self.assertEqual(result, "no data found for this age")

    @patch("ProductionCode.datasource_compare.psycopg2.connect")
    def test_compare_by_age_error(self, mock_connect):
        '''tests the error is returned from compare_by_age when incorrect query'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.execute.side_effect = psycopg2.Error()
        ds = DataSourceCompare()
        result = ds.compare_by_age(25, "test_activity")
        self.assertEqual(result, None)

    @patch("ProductionCode.datasource_compare.psycopg2.connect")
    def test_get_hint_for_compare(self, mock_connect):
        '''tests that get_hint_for_compare returns correct activity name suggestions'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [("Sleeping",), ("Sleeplessness",)]
        ds = DataSourceCompare()
        result = ds.get_hint_for_compare("sleep")
        self.assertEqual(result, ["Sleeping", "Sleeplessness"])
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT activities FROM activities WHERE LOWER(activities) LIKE %s LIMIT 10",
            ("sleep%",)
        )
        self.mock_cursor.fetchall.assert_called_once()
        self.mock_cursor.close.assert_called_once()

    @patch("ProductionCode.datasource_compare.psycopg2.connect")
    def test_get_hint_for_compare_empty_input(self, mock_connect):
        '''Tests that get_hint_for_compare returns empty list for empty input.'''
        mock_connect.return_value = self.mock_conn
        ds = DataSourceCompare()
        result = ds.get_hint_for_compare("")
        self.assertEqual(result, [])
