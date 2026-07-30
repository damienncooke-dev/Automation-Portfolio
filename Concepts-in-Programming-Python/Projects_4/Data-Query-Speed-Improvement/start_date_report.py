#!/usr/bin/env python3


"""
This script will ask the user for 3 data points; the year, the month and the day in which to query for employee start date.  The script will retrieve data from a url in CSV format and
save the data into a dictionary with the keys set to the employee start date. The user input start date will be checked to see if it is later than the minimum lookup date and earlier than
the current date. The user input date will then be used to lookup employee record in the dictionary. If no record found, advance to the next date until all dates have been exhausted
and a list of the employees found is generated.  A count of the number of employees found will complete the report.

"""

import csv
import datetime as dt
import requests


FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
  """Interactively get the start date to query for."""

  print()
  print('Getting the first start date to query for.')
  print()
  print('The date must be greater than Jan 1st, 2018')
  year = int(input('Enter a value for the year: '))
  month = int(input('Enter a value for the month: '))
  day = int(input('Enter a value for the day: '))
  print()

  return dt.datetime(year, month, day)   # returns a date object

def get_file_lines(url):
  """Returns the lines contained in the file at the given URL"""

  # # Download the file over HTTP using API requests.get(). Set stream True so data is not read into all at once into memory.
  response = requests.get(url, stream=True)
  lines = []

  for line in response.iter_lines():    # iterates over the lines in 'requests.Response' object
    lines.append(line.decode("UTF-8"))  # append line to list, use UTF-8 decoding so data is converted from byte code
  return lines

def load_employee_data():
  data = get_file_lines(FILE_URL) # data returned as list
  reader = csv.reader(data[1:])  # skip header row and start read from second element
  employee_data = {}   # define empty dictionary for all employees with start dates meeting search criteria

  for row in reader:
    row_date = row[3]
    # if row_date is not in dictionary, add it as the key with the current employee name.
    if row_date not in employee_data:
      employee_data[row_date] = [row[0] + " " + row[1]]
    else:
      # if row_date already exists, append the name of the current employee to the list of values for key=row_date
      # Format of dictionary item: {'row_date': ['(Name Surname)',...]}
      employee_data[row_date].append(row[0] + " " + row[1])

  return employee_data


def list_newer(start_date):
  min_date = dt.datetime.strptime("2018-1-1", '%Y-%m-%d')  # Absolute minimum date for searching
  employee_data = load_employee_data()   # dictionary of employee start dates
  employee_count = 0   # initialize counter for the number of employee records
  while start_date < dt.datetime.today() and start_date > min_date:
    emp_date = dt.datetime.strftime(start_date, "%Y-%m-%d")
    employees = employee_data.get(emp_date, [])  # lookup employee start date
    if len(employees) == 0:
      start_date = start_date + dt.timedelta(days=1)   # Advance date + 1
      continue
    else:
      print("Started on {}: {}".format(emp_date, employees))
      employee_count += len(employees)
      start_date = start_date + dt.timedelta(days=1)   # Advance date + 1
  print("The number of employees found: ", employee_count)


def main():
  start_date = get_start_date()
  list_newer(start_date)

if __name__ == "__main__":
  main()


""" RUNTIME:

/usr/local/bin/python3.14 /Users/admin/PycharmProjects/PythonProject/Coursera_GoogleITAutomation_Projects/Projects_4/Data-Query-Speed-Improvement/start_date_report.py 

Getting the first start date to query for.

The date must be greater than Jan 1st, 2018
Enter a value for the year: 2020
Enter a value for the month: 5
Enter a value for the day: 21

Started on 2020-05-22: ['Gemma Booker']
Started on 2020-05-28: ['Blake Franco']
Started on 2020-06-02: ['Kyle Roach']
Started on 2020-06-04: ['Tanek Edwards']
Started on 2020-06-06: ['Liberty Pena']
Started on 2020-06-10: ['Kyra Vance']
Started on 2020-06-11: ['Kiona Nguyen']
Started on 2020-06-13: ['Aurora Sanford']
Started on 2020-06-20: ['Jarrod Nicholson']
Started on 2020-06-24: ['Nicholas Brock']
Started on 2020-06-25: ['Quynn Parsons', 'Katell Gill']
Started on 2020-06-27: ['Melanie David', 'Jordan Golden']
Started on 2020-06-28: ['Xyla Ferrell']
Started on 2020-06-29: ['Kelsey Adkins']
Started on 2020-06-30: ['Grant Daugherty']
The number of employees found:  17

Process finished with exit code 0



"""