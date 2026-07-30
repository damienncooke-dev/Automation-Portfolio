#!/usr/bin/env python3

""" This script matches users to an email address by taking first name and last name as arguments
  and returns a formatted email address. This script has an accompanying test script for validation called
  test_emails.py.

  This script consists of two functions: populate_dictionary(filename) and find_email(argv).
  The function populate_dictionary(filename) reads the user_emails.csv file and populates a dictionary with name/value pairs.
  The other function, find_emails(argv), searches the dictionary created in the previous function for the user name
  passed to the function as a parameter. It then returns the associated email address.
  This script accepts employee's first name and last name as command-line arguments and outputs their email address.

  The script accepts arguments through the command line. These arguments are stored in a list named sys.argv.
  The first element of this list, i.e. argv[0], is always the name of the file being executed.
  So the parameters, i.e., first name and last name, are then stored in argv[1] and argv[2] respectively.  """

import sys
import csv
from pathlib import Path

def populate_dictionary(filename):
    """ Populate a dictionary with the name/email pairs for easy lookup"""
    email_dict = {}  # Create empty dictionary to store the name/email pairs
    with open(filename, 'r') as csvfile:   # Open the CSV file for reading
        lines = csv.reader(csvfile, delimiter=',')   # Read the entire file and create a read object called lines
        next(lines)   # skip the first row since it is just header information
        for row in lines:   # Iterate over the read object and extract line as list of name and email address
            name = str(row[0].lower())  # remove case inconsistencies for dict key
            email_dict[name] = row[1]  # store email address using full name as dict key 'name'
        return email_dict

def find_email(argv):
    """ Return an email address based on the username given."""
    # It is good practice to define paths within the method they will be used in case you write unit tests for that method
    base_dir = Path(__file__).resolve().parent
    user_emails = base_dir.parent / "data" / "user_emails.csv"
    try:
        fullname = str(argv[1] + " " + argv[2])  # arguments taken as script parameters as first and last name, space separated
        # Call populate_dictionary to get the dictionary of name/email pairs
        email_dict = populate_dictionary(user_emails)
        # If the email exists, print it
        if email_dict.get(fullname.lower()):
            return email_dict.get(fullname.lower())
        else:
            return "No email address found"
    except IndexError:
        return "Missing parameters"

def main():
    print(find_email(sys.argv))

if __name__ == "__main__":
    main()


"""RUNTIME
Run with in-line script parameters: emails.py Damien Cooke

/Users/admin/PyCharmMiscProject/.venv/bin/python /Users/admin/Coursera/Projects_2/Unit-Testing-Email-Lookup-Script/scripts/emails.py Damien Cooke 
damien.n.cooke@gmail.com

Process finished with exit code 0

"""