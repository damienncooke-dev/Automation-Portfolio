"""
This script takes a CSV file containing user emails, identifies email addresses with a specific old domain,
and replaces that domain with a new domain. It then saves the updated user data with the modified email addresses
to a new CSV report file.
"""

import csv
import re
from pathlib import Path



# This function checks for matches of the old domain in the file, return True if match, and False if no match
def contains_domain(address, domain):
    if re.search(domain, address):  # if domain in address, then match object is returned, otherwise False
        return True
    return False

# This function replaces the old domains with the new domains using regex .sub()
def replace_domain(address, old_domain, new_domain):
    address = re.sub(old_domain, new_domain, address)  # (regex, repl, email) --> ('abc.edu', 'xyz.edu', 'full_name@abc.edu')
    return address  # 'full_name@xyz.edu'

def main():
    """Process the list of emails, replacing any instances of the old domain with the new domain."""
    script_root_dir = Path(__file__).parent.parent
    old_domain, new_domain = "abc.edu", "xyz.edu"
    input_csv_file = script_root_dir / 'data' / 'user_emails.csv'
    output_report_file = script_root_dir / 'data' / 'updated_user_emails.csv'
    old_domain_email_list = []  # Read the user_emails.csv file and store emails here.
    new_domain_email_list = []  # Contains list of updated emails
    # Get the list of user emails from the CSV file
    with open (input_csv_file, 'r') as f:
        user_data_list = list(csv.reader(f))   # creates a list of 'lists' containing the rows of the csv file as [['Full Name, Email Address'], [...],[...]]
        user_email_list = (data[1].strip() for data in user_data_list[1:])  # iterate over user_data_list starting at row pos 1. Extract email addresses
        # Find the email addresses with the old domain, save the old domain email addresses as well as the updated email addresses
        for email_address in user_email_list:
            if contains_domain(email_address, old_domain):  # if email contains old domain then True
                old_domain_email_list.append(email_address)  # True: save the email address to old email list
                replaced_email = replace_domain(email_address, old_domain, new_domain)  # replace the old domain with new domain and returns email address with new domain
                new_domain_email_list.append(replaced_email) # save the updated email address to new email list
        # Get the index position of the email column. Getting the index position instead of setting it is protecting in case other columns are added to the file or the position changes.
        email_key = ' ' + 'Email Address'  # email_key = ' Email Address', add ' ' due to space after comma in the input email file.
        email_index = user_data_list[0].index(email_key)  # finds the position of ' Email Address' and returns index position, email_index = 1
        # From the original email list, check each record if it matches 'old domain', if true, update the original email list with the new domain.
        for user in user_data_list[1:]:  # starting from row 1 of the original email list, get every record for ['Full Name', ' Email Address']
            for old_domain, new_domain in zip(old_domain_email_list, new_domain_email_list):  # zip() function allows you to iterate over two lists simultaneously.
                if user[email_index] == ' ' + old_domain:  # if email from original email list is in old_domain email list then update the domain.
                    user[email_index] = ' ' + new_domain   # 'mutate' or update 'user_data_list' in place to take on the new_domain values
    # Write the new updated email list with new domain to output file.
    with open (output_report_file, 'w+') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(user_data_list)
        output_file.close()

if __name__ == "__main__":
    main()










