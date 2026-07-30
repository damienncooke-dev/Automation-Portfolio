# HR Report - Employee Count by Department

## Executive Summary
This script automates the monthly generation of an HR report to tally the number of employees in each department.  It eliminates manual overhead to import a CSV file into a spreadsheet,
creating pivot tables and functions to analyze the data, and then create a report. 

## System Architecture and Workflow
1. **Data Input** -The script reads an input file in CSV format, with strict dialect validation, containing the employee data.
2. **Data Processing** -The script counts the number of employees in each department and stores the results in a dictionary. 
3. **Data Output** -The script iterates over the sorted dictionary and writes to a text file that will contain the department with the number of employees in alphabetical order.

There are no hard-coded paths, the script resolves all the file paths dynamically relative to the script's root directory. Making the script portable across environments.

## Key Features and Components
* **Automated Data Parsing** -The script reads the CSV file using Python's CSV library.
* **Dynamic Path Resolution** -Uses Python's `pathlib` module to resolve file paths dynamically. No hard-coded paths and portable. 
* **Graceful Error Handling** -Catches `FileNotFoundError` and generates actionable output rather than crashing the script.
* **Data Aggregation and Processing** -Count the number of occurrences each department name shows up in the list. Aggregates data into a dictionary to keep track of the count by department.
* **Data Output** -Writes an alphabetically sorted output to a text file that has the department with the number of employees.

## Built With
* **Language** -Python 3.14
* **Libraries** -Standard libraries: `csv`, `pathlib`
* **Data Formats** -Input: CSV, Output: Text

## Getting Started
Follow the steps below to run this project locally. No external dependencies or packages are required.

## Prerequisites
* Python 3.14 or higher
    * Verify your python version
        ```python
            python3 --version
        ```
* A terminal / command-line interface
* Git (to clone the repository)

## Installation & Setup

1. Clone the repository.

```python
    git clone https://github.com/damienncooke-dev/IT-Automation-with-Python.git
    cd HR-Report-Employee-by-Department
```

2. Verify the expected directory structure.

```
    NOTES: 
    1. Ignore the helper_scripts directory. It is not part of the project and only used for conceptual testing. 
    2. Ignore the requirements.txt file. No requirements needed. 
    
HR-Report-Employee-by-Department/
├── data/
│   └── employees.csv
├── helper_scripts/
│   └── convertDictToCVS.txt
│   └── employees.dict.orig.txt
├── reports/
├── scripts/
│   └─generate_report.py
├── requirements.txt
├── README.md
```

3. Ensure your input file is in place. The script expects `user_emails.csv` to be in the `data` directory. The input file should follow this format:

```python
Full Name, Email Address
John Doe, jdoe, Engineering
Jane Smith, jsmith, Marketing
...
```

4. Run the script from the scripts directory:

```python
python3 generate_report.py

```

5. Upon successful execution, check the `reports` directory for the generated report:

```python
cat ../reports/report.txt
```

```
[OUTPUT:]

Development: 4
Human Resources: 2
IT infrastructure: 4
Marketing: 2
Sales: 3
User Experience Research: 2
Vendor operations: 2
```

6. Error Handling - The following error handling is implemented:

```
Scenario: Missing Input Data 
System Behavior: Catches `FileNotFoundError` and generates actionable output
Output Generated: File not found, check directory 'HR-Report-Employee-by-Department/data/employee.csv' and try again!
```
