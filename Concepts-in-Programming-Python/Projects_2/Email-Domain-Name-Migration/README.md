# Email Domain Name Migration

## Executive Summary
A new email domain has been created, and students using the old domain need to be migrated to the new domain. This script will read a file of students who may have the old domain that need to be migrated to the new domain. 

## System Architecture and Workflow
1. **Data Input** -Read an input file in CSV format containing student names and email addresses.
2. **Data Processing** -Find email addresses with old domain names and replace them with the new domain name.  
3. **Data Output** -Write the modified email list to a new file in CSV format. 

There are no hard-coded paths, the script resolves all the file paths dynamically relative to the script's root directory. Making the script portable across environments.

## Key Features and Components
* **Automated Data Parsing** -The script reads the CSV file using Python's CSV library.
* **Dynamic Path Resolution** -Uses Python's `pathlib` module to resolve file paths dynamically. No hard-coded paths and portable. 
* **Regular Expression Matching** -Uses regular expressions 're' module and '.sub()' method to search and replace the old domain with the new domain.
* **Data Aggregation and Processing** -Searches for old domain names in the original email list. Create two lists with the old domain and new domain email addresses. Compares the original email list to the old domain email list and modifies the original email list with the new domain email address when old domain is found.
* **Data Output** -Writes the modified email list to a new CSV file in the same directory as the original CSV file.

## Built With
* **Language** -Python 3.14
* **Libraries** -Standard libraries: `csv`, `pathlib`, `re`
* **Data Formats** -Input: **CSV**, Output: **CSV**

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
    cd Email-Domain-Name-Migration
```

2. Verify the expected directory structure.

```
    NOTES: 
    1. Ignore the helper_scripts directory. It is not part of the project and only used for conceptual testing. 
    2. Ignore the requirements.txt file. No requirements needed. 
    
HR-Report-Employee-by-Department/
├── data/
│   └── user_emails.csv
├── scripts/
│   └─replace_email_domain.py
├── requirements.txt
├── README.md
```

3. Ensure your input file is in place. The script expects `employees.csv` to be in the `data` directory. The input file should follow this format:

```python
Full Name, Email Address
Blossom Gill, blossom@abc.edu
Hayes Delgado, nonummy@utnisia.com
...
```

4. Run the script from the scripts directory:

```python
python3 replace_email_domain.py

```

5. Upon successful execution, check for the file `updated_user_emails.csv` the `data` directory:

```python
ls -l ../data/updated_user_emails.csv
```
... check that the email addresses have been updated to the new domain and that the old domain has been removed from the updated list...

```
[OUTPUT:]

(.venv) admin@Damiens-MacBook-Pro data % grep 'abc.edu' user_emails.csv| wc -l
      10
(.venv) admin@Damiens-MacBook-Pro data % grep 'xyz.edu' updated_user_emails.csv| wc -l
      10
(.venv) admin@Damiens-MacBook-Pro data % grep 'abc.edu' updated_user_emails.csv| wc -l
       0

```


