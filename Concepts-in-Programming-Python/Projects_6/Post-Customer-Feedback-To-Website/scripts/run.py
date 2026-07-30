#!/usr/bin/env python3

""" This script will read through a list of files that contain customer feedback
on their experience with buying second hand cars at a dealership. Each file represents
feedback fron one customer.  So each file contains data that will be stored in a dictionary
where the keys are title, name, date, feedback.  Therefore the structure will be a list of
dictionaries.
"""

# Import Path from pathLib to handle file paths
from pathlib import Path
# Import requests for making HTTP requests
import requests
import os

feedback_dir = Path(__file__).parent.parent / "data" / "feedback"

# Get a list of the files from data/feedback
feedback_files = [file.name for file in feedback_dir.iterdir()]

# This list will hold dictionaries of feedback data read from each file in data/feedback
feedback = []

for file in feedback_files:
    fpath = os.path.join(feedback_dir, file)
    with open(fpath, 'r') as f:
        # Append to the list, the entries of the dictionary. NOTE: readline and read picks up from where the last read took place. Remember to strip away new line.
        feedback.append({"title":f.readline().rstrip("\n"),
                         "name":f.readline().rstrip("\n"),
                         "date":f.readline().rstrip("\n"),
                         "feedback":f.read().rstrip("\n")}).  # Last line performs a 'read()' which reads till end of file.

for record in feedback:
    # Post the item to the website using "request.post" and save the response from the server and flag item as json
    resp = requests.post('http://35.229.26.76:80/feedback/', json=record)
    # For a succeful POST operation we expect the response code to be 201, if not raise Exception
    if resp.status_code != 201:
        raise Exception("POST error status={}".format(resp.status_code))
    print("Created feedback ID: {}".format(resp.json()["id"]))

#======= OUTPUT ======
""" RUNTIME
student@50705e6170d7:~$ ./run.py 
Created feedback ID: 16
Created feedback ID: 17
Created feedback ID: 18
Created feedback ID: 19
Created feedback ID: 20 

"""











