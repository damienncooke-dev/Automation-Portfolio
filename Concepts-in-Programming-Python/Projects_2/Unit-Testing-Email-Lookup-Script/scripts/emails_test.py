#!/usr/bin/env python3

""" This will be the test cases for emails.py. Begin by importing unittest. The unittest package supports
test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and
independence of the tests from the reporting framework.  This module also provides classes that make it
simple to support these qualities for a set of tests"""

import unittest

# The following import statement allows a Python file to access the script from another Python file. In this
# case, we will import the function find_email, which is defined in the script emails.py
from emails import find_email

# Now we have to create a class that inherits from unittest.TestCase. This class will contain the test cases.
# Classes are a way to bundle data and functionality together. Creating a new class creates a new object,
# which will further allow new instances of that type to be made.
class EmailsTest(unittest.TestCase):

    # A test case is created by subclassing unittest.TestCase. This is the first basic test case
    def test_basic(self):
        testcase = [None, "Bree", "Campbell"]    # input for the test, None is used for the sys.argv[0]
        expected = "breee@utnisia.net"
        self.assertEqual(find_email(testcase), expected)  # call the function being tested with testcase argument. then state the expected result

    def test_one_name(self):
        testcase = [None, "John"]    # input for the test
        expected = "Missing parameters"
        self.assertEqual(find_email(testcase), expected)  # call the function being tested with testcase argument. then state the expected result

    def test_two_name(self):
        testcase = [None, "Roy", "Cooper"]    # input for the test
        expected = "No email address found"
        self.assertEqual(find_email(testcase), expected)  # call the function being tested with testcase argument. then state the expected result


if __name__ == "__main__":
    unittest.main()



""" RUNTIME:
/Users/admin/PyCharmMiscProject/.venv/bin/python /Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm/_jb_unittest_runner.py --path /Users/admin/Coursera/Projects_2/Unit-Testing-Email-Lookup-Script/scripts/emails_test.py 
Testing started at 12:15 PM ...
Launching unittests with arguments python -m unittest /Users/admin/Coursera/Projects_2/Unit-Testing-Email-Lookup-Script/scripts/emails_test.py --quiet in /Users/admin/Coursera/Projects_2/Unit-Testing-Email-Lookup-Script/scripts



Ran 3 tests in 0.001s

OK

Process finished with exit code 0


"""



