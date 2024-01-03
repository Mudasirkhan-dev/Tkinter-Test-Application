import unittest
import requests

class TestEmployeeAPI(unittest.TestCase):
    def setUp(self):
        # Set up the base URL for the API
        self.base_url = 'http://localhost:5000/employees'

    def test_1_add_employee(self):
        # Test adding a new employee
        new_employee_data = {
            'emp_id': 'E001',
            'emp_name': 'John Doe',
            'mobile': '1234567890',
            'salary': 50000
        }

        response = requests.post(self.base_url, json=new_employee_data)
        self.assertEqual(response.status_code, 201)

    def test_2_get_employees(self):
        # Test retrieving all employee records
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        employees = response.json()
        self.assertIsInstance(employees, list)

    def test_3_update_employee(self):
        # Test updating an existing employee record
        update_data = {
            'emp_name': 'Updated Name',
            'mobile': '9876543210',
            'salary': 60000
        }

        emp_id = 'E001'
        response = requests.put(f'{self.base_url}/{emp_id}', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_4_delete_employee(self):
        # Test deleting an existing employee record
        emp_id = 'E001'
        response = requests.delete(f'{self.base_url}/{emp_id}')
        self.assertEqual(response.status_code, 200)

    def test_5_delete_nonexistent_employee(self):
        # Test deleting a nonexistent employee record
        emp_id = 'NonExistentID'
        response = requests.delete(f'{self.base_url}/{emp_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
