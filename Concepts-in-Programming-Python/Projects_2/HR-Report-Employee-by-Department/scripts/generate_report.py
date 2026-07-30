#! /usr/bin/env python3
"""
This script automates the monthly generation of an HR report to tally the number of employees in each department.  It eliminates manual overhead to import a CSV file into a spreadsheet,
creating pivot tables and functions to analyze the data, and then create a report.

This script will read a CSV file with employee name, user_name, and department. It uses a dictionary in which to tally the number of employees in a department.
Finally, a report will be generated with the total number of people in each department and written to a text file 'reports.txt'
"""

import csv
from pathlib import Path


def read_employees(csv_file_location):
    csv.register_dialect('empDialect', skipinitialspace=True, strict=True)  # ignore spaces after delimiter, and raise an error if 'strict' formatting is not used.
    employee_list = [] # define list to hold employee file records from 'csv_file_location'
    try:
        with open(csv_file_location, 'r') as csv_file:
            employee_file = csv.DictReader(csv_file,dialect='empDialect')  # creates an object containing list of dictionary items, by default first row of file are the dict keys if no 'fieldnames' provided
            for data in employee_file:  # iterate over object and extract each dictionary record row
                employee_list.append(data)  # append each dictionary item to the list.
    except FileNotFoundError:
        print("File not found, check directory '{}' and try again!".format(csv_file_location))
    return employee_list   # returns a list of dictionary items

def process_data(employee_list):
    department_list = []
    for employee in employee_list:   # iterate over the list of dictionary items, extracting employee records with department values
        department_list.append(employee['Department'])  # append department values to a new list of departments
    department_data = {}  # define a dictionary to store the departments
    for department_name in set(department_list):   # use set() to remove duplicate department values from the list
        department_data[department_name] = department_list.count(department_name)  # use .count() method to count the number of times a department appears in the list, and store in dictionary
    return department_data   # returns a dictionary of department names and the number of times the department

def write_report(dictionary, report_file):
    rep_file = report_file
    with open(rep_file, 'w') as f:
        for k in sorted(dictionary):  # for each key in sorted dictionary
            f.write(str(k) + ": " + str(dictionary[k]) + "\n")   # write 'department' : 'employee count' to report file'


# Putting it all together
if __name__ == "__main__":
    script_root_dir = Path(__file__).parent.parent  # define script root directory relative to script directory
    data_dir = script_root_dir / 'data'   # directory with input CSV file
    reports_dir = script_root_dir / 'reports'  # output directory
    input_file = data_dir / 'employees.csv'  # CSV file with employee name, user_name, and department
    output_file = reports_dir / 'report.txt'  # output report file with department names and number of employees
    employee_list = read_employees(input_file)
    emp_count_dict = process_data(employee_list)
    write_report(emp_count_dict, output_file)















