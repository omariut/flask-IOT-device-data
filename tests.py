import unittest
from datetime import datetime
from main import app
from utils import get_validated_data

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_post_data_valid(self):
        data = [
            "1649941817 Voltage 1.34",
            "1649941818 Voltage 1.35",
            "1649941817 Current 12.0",
            "1649941818 Current 14.0"
        ]
        response = self.client.post('/data', data='\n'.join(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'success': True})

    def test_post_data_invalid(self):
        data = [
            "1649941817 Voltage 1.34",
            "1649941818 Voltage 1.35",
            "1649941819 Current 14.0"
        ]
        response = self.client.post('/data', data='\n'.join(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'success': False})

    def test_get_data_all(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertIsInstance(data, list)  # Verify that the response is a list

        # Verify the structure of each item in the list
        for item in data:
            self.assertIsInstance(item, dict)  # Verify that each item is a dictionary
            self.assertIn('time', item)  # Verify the presence of 'time' key
            self.assertIsInstance(item['time'], str)  # Verify the value of 'time' is a string
            self.assertIn('name', item)  # Verify the presence of 'name' key
            self.assertIsInstance(item['name'], str)  # Verify the value of 'name' is a string
            self.assertIn('value', item)  # Verify the presence of 'value' key
            self.assertIsInstance(item['value'], (int, float))  # Verify the value of 'value' is a number

 


if __name__ == '__main__':
    unittest.main()
