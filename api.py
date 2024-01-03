from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']
employees_collection = db['employees']

# Route to get all employee records
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = list(employees_collection.find({}, {'_id': 0}))
    return jsonify(employees)

# Route to add a new employee record
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json

    emp_id = data.get('emp_id')
    emp_name = data.get('emp_name')
    mobile = data.get('mobile')
    salary = data.get('salary')

    if not emp_id or not emp_name or not mobile or not salary:
        return jsonify({'error': 'All fields are required'}), 400

    new_employee = {
        'emp_id': emp_id,
        'emp_name': emp_name,
        'mobile': mobile,
        'salary': salary
    }

    employees_collection.insert_one(new_employee)
    return jsonify({'message': 'Employee added successfully'}), 201

# Route to update an existing employee record
@app.route('/employees/<string:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.json

    emp_name = data.get('emp_name')
    mobile = data.get('mobile')
    salary = data.get('salary')

    result = employees_collection.update_one(
        {'emp_id': emp_id},
        {'$set': {'emp_name': emp_name, 'mobile': mobile, 'salary': salary}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Employee updated successfully'})

    return jsonify({'error': 'Employee not found'}), 404

# Route to delete an employee record
@app.route('/employees/<string:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    result = employees_collection.delete_one({'emp_id': emp_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Employee deleted successfully'})

    return jsonify({'error': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
