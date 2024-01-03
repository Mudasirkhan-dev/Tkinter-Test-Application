import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to submit form data to the Flask API
def submit_form():
    emp_id = entry_emp_id.get()
    emp_name = entry_emp_name.get()
    mobile = entry_mobile.get()
    salary = entry_salary.get()

    # Validate if all fields are filled
    if not emp_id or not emp_name or not mobile or not salary:
        messagebox.showerror("Error", "All fields are required")
        return

    # Prepare data to send to the API
    data = {
        "emp_id": emp_id,
        "emp_name": emp_name,
        "mobile": mobile,
        "salary": salary
    }

    # Send a POST request to the API endpoint
    response = requests.post("http://localhost:5000/employees", json=data)

    if response.status_code == 201:
        # Add data to the tree view
        tree.insert("", tk.END, values=(emp_id, emp_name, mobile, salary))

        # Display the submitted information
        message = f"Employee ID: {emp_id}\nEmployee Name: {emp_name}\nMobile: {mobile}\nSalary: {salary}"
        messagebox.showinfo("Registration Successful", message)

        # Show data inserted successfully message
        messagebox.showinfo("Success", "Data inserted successfully")

        # Clear the entry fields
        clear_fields()
    else:
        messagebox.showerror("Error", f"Failed to submit data. Status code: {response.status_code}")

# Function to update the selected record using the Flask API
def update_record():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a record to update")
        return

    # Get values from the selected item
    values = tree.item(selected_item, "values")
    emp_id, _, _, _ = values  # We only need the employee ID for the update

    # Prepare data to send to the API
    data = {
        "emp_name": entry_emp_name.get(),
        "mobile": entry_mobile.get(),
        "salary": entry_salary.get()
    }

    # Send a PUT request to the API endpoint for the specific employee
    response = requests.put(f"http://localhost:5000/employees/{emp_id}", json=data)

    if response.status_code == 200:
        # Update the tree view with the modified data
        tree.item(selected_item, values=(emp_id, entry_emp_name.get(), entry_mobile.get(), entry_salary.get()))

        # Show update successful message
        messagebox.showinfo("Success", "Record updated successfully")
        clear_fields()
    else:
        messagebox.showerror("Error", f"Failed to update record. Status code: {response.status_code}")

# Function to delete the selected record using the Flask API
def delete_record():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete")
        return

    # Get the employee ID from the selected item
    emp_id = tree.item(selected_item, "values")[0]

    # Send a DELETE request to the API endpoint for the specific employee
    response = requests.delete(f"http://localhost:5000/employees/{emp_id}")

    if response.status_code == 200:
        # Delete the selected item from the tree view
        tree.delete(selected_item)

        # Clear the entry fields
        clear_fields()

        # Show delete successful message
        messagebox.showinfo("Success", "Record deleted successfully")
    else:
        messagebox.showerror("Error", f"Failed to delete record. Status code: {response.status_code}")

# Function to clear entry fields
def clear_fields():
    entry_emp_id.delete(0, tk.END)
    entry_emp_name.delete(0, tk.END)
    entry_mobile.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

def show_record():
    # Send a GET request to the API endpoint to fetch all employee records
    response = requests.get("http://localhost:5000/employees")
    
    if response.status_code == 200:
        # Clear existing data in the tree view
        for item in tree.get_children():
            tree.delete(item)

        # Retrieve and insert new data into the tree view
        employees = response.json()
        for employee in employees:
            tree.insert("", tk.END, values=(employee['emp_id'], employee['emp_name'], employee['mobile'], employee['salary']))
    else:
        messagebox.showerror("Error", f"Failed to fetch records. Status code: {response.status_code}")


# Create the main window
root = tk.Tk()
root.title("Employee Registration Form")

# Create labels
label_emp_id = tk.Label(root, text="Employee ID:")
label_emp_name = tk.Label(root, text="Employee Name:")
label_mobile = tk.Label(root, text="Mobile:")
label_salary = tk.Label(root, text="Salary:")

# Create entry widgets
entry_emp_id = tk.Entry(root)
entry_emp_name = tk.Entry(root)
entry_mobile = tk.Entry(root)
entry_salary = tk.Entry(root)

# Create buttons
submit_button = tk.Button(root, text="Submit", command=submit_form)
update_button = tk.Button(root, text="Update", command=update_record)
delete_button = tk.Button(root, text="Delete", command=delete_record)
show_button = tk.Button(root, text="Show", command=show_record)

# Create TreeView
tree = ttk.Treeview(root, columns=("Employee ID", "Employee Name", "Mobile", "Salary"), show="headings")
tree.heading("Employee ID", text="Employee ID")
tree.heading("Employee Name", text="Employee Name")
tree.heading("Mobile", text="Mobile")
tree.heading("Salary", text="Salary")

# Grid layout
label_emp_id.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_emp_id.grid(row=0, column=1, padx=10, pady=10)
label_emp_name.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_emp_name.grid(row=1, column=1, padx=10, pady=10)
label_mobile.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_mobile.grid(row=2, column=1, padx=10, pady=10)
label_salary.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
entry_salary.grid(row=3, column=1, padx=10, pady=10)

submit_button.grid(row=4, column=0, pady=20, padx=5)
update_button.grid(row=4, column=1, pady=20, padx=5)
delete_button.grid(row=4, column=2, pady=20, padx=5)
show_button.grid(row=5, column=0, pady=20, padx=5)

tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Start the main loop
root.mainloop()
