#!/usr/bin/env python3

"""
This script will ask the user for 3 data points; the year, the month and the day in which to query for employee start date.  The script will retrieve data from a url in CSV format.
The data will be read line by line and tested for the minimum date and whether the date falls in between the requested search date and the current day's date.
If the retrieved date meets the criteria, the employee name is added to the list along with the start date. The search will continue for a lower start date if it exists.
If a lower date is found, the list is reset and the employee information is added to the list. This will continue until the lowest date meeting the search criteria is found,
the start date is advanced by 1 day and the process is repeated until there are no more dates meeting the search criteria.  A count of the number of employees found will complete the report.

"""

import csv
from datetime import datetime
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

  return dt.datetime(year, month, day)  # returns a date object

def get_file_lines(url):
  """Returns the lines contained in the file at the given URL"""

  # Download the file over HTTP using API requests.get(). Set stream True so data is not read into all at once into memory.
  response = requests.get(url, stream=True)
  lines = []

  for line in response.iter_lines():  # iterates over the lines in 'requests.Response' object
    lines.append(line.decode("UTF-8"))  # append line to list, use UTF-8 decoding so data is converted from byte code
  return lines

def get_same_or_newer(start_date):
  """This function will check each line of data, confirming that the date is lower than the current minimum set date.
  The purpose is to keep finding the lowest date in the list on each pass, appending all employees starting on that date.
  When the function ends, the search begins again and keeps going until there are no more dates between the requested
  start date and the current day's date."""
  data = get_file_lines(FILE_URL)  # data returned as list
  reader = csv.reader(data[1:])  # skip header row and start read from second element

  # We want all employees that started at the same date or the closest newer
  # date. To calculate that, we go through all the data and find the
  # employees that started on the smallest date that's equal or bigger than
  # the given start date.
  min_date = dt.datetime.today()
  min_date_employees = []
  for row in reader:
    # Format of 'row' data: [Name,Surname,Department,Start Date]
    row_date = dt.datetime.strptime(row[3], '%Y-%m-%d')  # takes the date string "Start Date" and turns it into date object: 'row_date'

    # If the row_date is less than our requested start_date then we skip the row and get next row
    # If the row_date is greater than our requested start_date then we move forward with the search
    if row_date < start_date:
      continue

    if row_date < min_date:    # If row_date == min_date, date is still minimum date. Bypass and continue search
      min_date = row_date      # If row_date is less than the current 'min_date', set row_date as the current min_date
      min_date_employees = []  # New min_date found, reset list and continue searching

    if row_date == min_date:
      min_date_employees.append("{} {}".format(row[0], row[1]))

  return min_date, min_date_employees

def list_newer(start_date):
  min_date = dt.datetime.strptime("2018-1-1", '%Y-%m-%d') # Absolute minimum date for searching
  employee_count = 0
  while start_date < dt.datetime.today() and start_date > min_date:
    start_date, employees = get_same_or_newer(start_date)
    if len(employees) != 0:
        print("Started on {}: {}".format(start_date.strftime("%b %d, %Y"), employees))
        employee_count += len(employees)
    # Advance start date by one day and restart another search.
    start_date = start_date + dt.timedelta(days=1)
  print("The number of employees found: ", employee_count)
def main():
  start_date = get_start_date()  # start_date is now date object
  list_newer(start_date)

if __name__ == "__main__":
  main()


""" RUNTIME:

/usr/local/bin/python3.14 /Users/admin/PycharmProjects/PythonProject/Coursera_GoogleITAutomation_Projects/Projects_4/Data-Query-Speed-Improvement/start_date_report.py 

Getting the first start date to query for.

The date must be greater than Jan 1st, 2018
Enter a value for the year: 2019
Enter a value for the month: 3
Enter a value for the day: 3

Started on Mar 03, 2019: ['Martin Dalton']
Started on Mar 04, 2019: ['Gage Vega']
Started on Mar 05, 2019: ['Benjamin Blake']
Started on Mar 06, 2019: ['Xerxes James']
Started on Mar 11, 2019: ['Anne Giles']
Started on Mar 15, 2019: ['Fay Schroeder']
Started on Mar 17, 2019: ['Keaton Edwards']
Started on Mar 18, 2019: ['Sheila Richards']
Started on Mar 22, 2019: ['Jelani Fernandez']
Started on Mar 27, 2019: ['Walker Cline']
Started on Mar 29, 2019: ['Eleanor Dorsey']
Started on Mar 30, 2019: ['Kelly Dillon', 'Denise Wilkins']
Started on Apr 05, 2019: ['Lucas Fuentes']
Started on Apr 07, 2019: ['Taylor Butler']
...

Started on Jun 25, 2020: ['Quynn Parsons', 'Katell Gill']
Started on Jun 27, 2020: ['Melanie David', 'Jordan Golden']
Started on Jun 28, 2020: ['Xyla Ferrell']
Started on Jun 29, 2020: ['Kelsey Adkins']
Started on Jun 30, 2020: ['Grant Daugherty']
The number of employees found:  213

Process finished with exit code 0

"""