#! /usr/bin/env python3
"""
This is a log parser script to search a log file for user-specified errors. It prompts the user to enter the error message,
then iterates through each line of the log file, checking for matches against the specified error pattern.
If a match is found, the line is added to a list of found errors. Once the search is complete, the found errors are written
to a separate output file for further analysis. The script uses regular expressions for pattern matching and
provides flexibility in defining error patterns.

To test the script, run it with parameter: 'monitor.log', then at the prompt enter: 'CRON ERROR Failed to start'
"""


import sys
import re
from pathlib import Path


def error_search(log_file):
    returned_errors = []  # define empty list to store the found errors
    error = input("What is the error? ")   # get user input for the error message
    error_patterns = [re.escape(word) for word in error.split()]  # split the error message into a list of error patterns and escape any metacharacters
    print(error_patterns)
    try:
        with open(log_file, mode='r',encoding='UTF-8') as file:  # general best practice to open log file with encoding UTF-8
            for log in file.readlines():
                log_lower = log.lower()  # for each line in the log file lower the case to avoid having any case match issues.
                if all(re.search(pattern.lower(), log_lower) for pattern in error_patterns):  # for each item in error_pattern, search line from log file for a match, return True if all elements match
                    returned_errors.append(log)  # append the log file line to 'returned_errors' list.
    except FileNotFoundError:
        print("File not found, check directory for '{}' and try again!".format(log_file))
        sys.exit(1)
    return returned_errors    # return list of found errors, if no errors are found, the list will be empty.

def file_output(returned_errors):
    print("Found {} errors:".format(len(returned_errors)))
    print("\n".join(returned_errors))
    errors_found_log = script_root_dir / 'data' / "errors_found.log"
    with open(errors_found_log, 'w', encoding='UTF-8') as file:
        for error in returned_errors:
            file.write(error)
        file.close()

if __name__ == "__main__":
    script_root_dir = Path(__file__).parent.parent
    try:
        log_file = script_root_dir / "data" / sys.argv[1]  # log file name provided as a command-line argument
        returned_errors = error_search(log_file)  # find and return error
        file_output(returned_errors)  # write error to output file for review
    except IndexError:
        print("Please provide a log file name as a command-line argument.")
    sys.exit(0)



""" RUNTIME:
What is the error? CRON ERROR Failed to start
['CRON', 'ERROR', 'Failed', 'to', 'start']
Found 1 errors:
July 31 04:11:32 mycomputername CRON[51253]: ERROR Failed to start CRON job due to script syntax error. Inform the CRON job owner!


Process finished with exit code 0

"""

