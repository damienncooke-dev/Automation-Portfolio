#!/usr/bin/env python3

"""
The context for this script is that it will aggregate log file statistics for a dashboard being developed for IT management.

This script will read the syslog file and extract the username, error message and log type (e.g. INFO|ERROR) for each log message. It will use the 're' module and re.search()
to apply a regular expression with group capturing.  The text of each log message will be stored in a dictionary and counted for how many times it appears in the log message.  Statistics
regarding the number of INFO and ERROR messages for each user will be stored in a separate dictionary. Both dictionaries will be sorted by value (most common to least common) for the
error messages and username (alphabetical) for the statistics. The output from both dictionaries will be written to CSV files called 'user_statistics.csv' and 'error_message.csv'.

"""

import re
import operator
from pathlib import Path

# Dict: Count number of entries for each user
per_user = {}
# Dict: Number of different error messages, where the messages are the keys
errors = {}

# Set base directory paths
base_dir = Path(__file__).resolve().parent
syslog = base_dir.parent / 'logs' / 'syslog.log'
user_stat = base_dir.parent / 'data' / 'user_statistics.csv'
error_messages = base_dir.parent / 'data' / 'error_message.csv'

# Read the syslog file and create dictionaries
with open(syslog, 'r') as file:
    for line in file.readlines():
        match = re.search(r'(INFO|ERROR)\s([\w\' ]+).*\(([a-z.]+)\)', line)
                # 1st capture group: (INFO|ERROR)=log_type, 2nd capture group: ([\w\' ]+)=error_msg, 3rd capture group: ([a-z.]+)=username
        log_type, error_msg, user = match.group(1), match.group(2), match.group(3)
        errors[error_msg] = errors.get(error_msg, 0) + 1.  # Checks if error_msg is in errors dict, if not, sets to 0, then adds 1.
        if user not in per_user.keys():
            per_user[user] = {'INFO': 0, 'ERROR': 0}   # Check if the user is in per_user dict, if not, add user as key and set INFO and ERROR to 0.
        if log_type == 'INFO':              # If log_type is INFO, add 1 to INFO count in per_user dict
            per_user[user]['INFO'] += 1
        elif log_type == 'ERROR':           # If log_type is ERROR, add 1 to ERROR count in per_user dict
            per_user[user]['ERROR'] +=1

# Sorted by Value (Most common to least common)
errors_list = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)   # Sort by value and reverse=True to sort in descending order

# Sorted by Username
per_user_list = sorted(per_user.items())  # Sort by username (default if key not specified)

print(errors_list)
print(per_user_list)

# * Create CSV file user_statistics
with open(user_stat, 'w', newline='') as user_csv:
    user_csv.write('Username,INFO,ERROR\n')  # Write header row to CSV file
    for key, value in per_user_list:  # Iterate over the list of user and dictionary pairs
        user_csv.write(str(key) + ',' + str(value['INFO']) + ',' + str(value['ERROR']) + '\n')


# * Create CSV error_message
with open(error_messages, 'w', newline='') as error_csv:
    error_csv.write('Error,Count\n')  # Write header row to CSV file
    for key, value in errors_list:  # Iterate over the list of tuples, 'error' and 'count'
        error_csv.write(str(key) + ',' + str(value) + '\n')





