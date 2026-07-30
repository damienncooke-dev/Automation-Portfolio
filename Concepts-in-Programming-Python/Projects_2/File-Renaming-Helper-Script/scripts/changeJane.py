#!/usr/bin/env python3

"""
The context for this script is that it is a helper script to be imported to another script. Its purpose is to rename a list of files based on a master text document with a list of files
Write a Python script, changeJane.py, that takes oldFiles.txt as a command line argument and then renames files with the new username jdoe.
The oldFiles.txt is created as output from findJane.sh bash script.
Use the OS command 'mv' to rename the files. Invoke the command using subprocess.run()
"""

# Import the modules needed to interact with the OS. Note: 'sys' stands for system-specific parameters and functions.
import sys
import subprocess


with open(sys.argv[1], 'r') as file:   # Open the oldFiles.txt file passed as a parameter to the script
    lines = file.readlines()
    for line in lines:
        oldvalue = line.strip()   # remove any new lines from string
        newvalue = oldvalue.replace('jane', 'jdoe')   # string replace 'old' value with 'new' value
        #subprocess.run(["mv", oldvalue, newvalue])  # rename file from oldvalue to newvalue
        subprocess.run(["echo", newvalue])  # for stdout purposes only
file.close()



""" RUNTIME:
/Users/admin/PyCharmMiscProject/.venv/bin/python /Users/admin/Coursera/Projects_2/File-Renaming-Helper-Script/scripts/changeJane.py oldFiles.txt 
../data/jdoe_profile_07272018.doc
../data/jdoe_pic_07282018.jpg
../data/jdoe_contact_07292018.csv

Process finished with exit code 0

"""
