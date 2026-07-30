#!/usr/bin/env python3

""" This script will backup files from 'src' to 'dest1' and 'dest2'.  Files copied to 'dest1' will be normal rsync copy and timed for completion.  Files
copied to dest2 will be using the multiprocessing 'Pool()' method to concurrently backup the files.  The difference should show that multiprocessing is faster way to archive files"""


import subprocess
import os
import time
from multiprocessing import Pool

# 'src' and 'dest' are relative paths
src = "/Users/admin/Desktop/Desktop Cleanup"
dest1 = "/Users/admin/Desktop/screenshot_archive_1"
dest2 = "/Users/admin/Desktop/screenshot_archive_2"


def backup_prod(bkup_files,dest):
    subprocess.run(["rsync", "-arq", bkup_files, dest])    # subprocess.call() is used to send linux commands to the OS.
    print("Syncing {} to prod_backup".format(bkup_files))

if __name__ == "__main__":  # This line is saying that everything below this line is to be only executed when ran directly and is to be ignored when imported.

# Set an empty list to hold files discovered by the os.walk() function.
# os.walk() will traverse the directory tree rooted at src and yield tuples of strings (dirpath, dirnames, filenames) for each directory it visits.
# Finally, we can use 'dirpath' and 'filename' with os.path.join to construct the full path of each file and append to list

    bkup_files = []
    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            bkup_files.append(os.path.join(dirpath, filename))

# This block of code is an example of concurrent processing using multiprocessing.Pool.
# First, you import the Pool class from multiprocessing.
# Then, you create a Pool object with 'x' number of processes.
# Finally, you call the map() method of the Pool object to execute the function you want to on each item in the list.
# Basically, "backup_prod" will be called for each item in the list, however each call will be executed concurrently, without waiting for the previous call to finish.
    start = time.perf_counter()
    [backup_prod(file,dest1) for file in bkup_files]
    end = time.perf_counter()
    print(f">>>>  Elasped time dest1: {end - start:.4f} second  <<<<")

    start = time.perf_counter()
    p = Pool(processes=4)  # There is a writeup in one note that is very useful for understanding how to use multiprocessing.Pool.
    p.starmap(backup_prod, [(file,dest2) for file in bkup_files])
    end = time.perf_counter()
    print(f">>>>  Elasped time dest2: {end - start:.4f} second. <<<<")


#=========== OUTPUT BELOW =================
""" RUNTIME:

/usr/local/bin/python3.14 /Users/admin/PycharmProjects/PythonProject/Coursera_GoogleITAutomation_Projects/Projects_4/Parallel-Rsync-With-Multiprocessing/dailysync.py 
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2019-11-10 at 1.39.31 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-07-05 at 11.10.10 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-12-15 at 5.56.06 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-01-28 at 5.05.26 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-07-02 at 5.05.42 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-12-03 at 2.02.32 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-07-14 at 12.38.53 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-04-23 at 3.31.07 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2023-09-18 at 11.30.54 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-09-21 at 8.48.06 AM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/IMG_0516.JPG to prod_backup
...
>>>>  Elasped time dest1: 0.5884 second  <<<<

Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-07-02 at 5.05.42 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-12-15 at 5.56.06 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-07-14 at 12.38.53 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-12-03 at 2.02.32 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-01-28 at 5.05.26 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2022-04-23 at 3.31.07 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2023-09-18 at 11.30.54 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2021-09-21 at 8.48.06 AM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2023-05-17 at 11.13.18 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2019-11-10 at 1.39.31 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/Screen Shot 2023-08-24 at 5.12.35 PM.png to prod_backup
Syncing /Users/admin/Desktop/Desktop Cleanup/IMG_0516.JPG to prod_backup
...
>>>>  Elasped time dest2: 0.2713 second. <<<<



INTERESTING OBSERVATION:
When the script is executed again without removing the files from the destination directory, the timing is about 
the same...

>>>>  Elasped time dest1: 0.3793 second  <<<<

>>>>  Elasped time dest2: 0.3664 second. <<<<

"""






