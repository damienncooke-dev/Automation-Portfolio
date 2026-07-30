#!/usr/bin/env python3

""" The multisync.py is for practice in order to
understand how multiprocessing works. We used the Pool class of the 
multiprocessing Python module. Here, we define a run method to perform the tasks. 
Next, we have a few tasks. Create a pool object of the Pool class of a 
specific number of CPUs your system has by passing a number of tasks you have. 
Start each task within the pool object by calling the map instance method, 
and pass the run function and the list of tasks as an argument. """


from multiprocessing import Pool

# Define a function
def run(task):
  print("Handling {}".format(task))

if __name__ == "__main__":
  # Tasks for parallel execution are generally in list format and then mapped to function.
  tasks = ['task1', 'task2', 'task3']
  # Create a pool object with specific number of CPUs e.g. Pool(4) or "Pool 4 CPUs"
  p = Pool(len(tasks))
  # Map each task or input to the function to be run in the pooled CPUs concurrently.
  p.map(run, tasks)


""" RUNTIME:

/usr/local/bin/python3.14 /Users/admin/PycharmProjects/PythonProject/Coursera_GoogleITAutomation_Projects/Projects_4/Parallel-Rsync-With-Multiprocessing/multisync.py 
Handling task1
Handling task2
Handling task3

Process finished with exit code 0


"""