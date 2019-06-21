import os
import getpass
import requests
import logging

from src.backend.expungeservice.crawler.crawler import Crawler
from src.backend.expungeservice.expunger.expunger import Expunger
from datetime import datetime


##############################################
PRODUCTION = True
##############################################

ERROR_LOG_FILE = 'Documents/RecordExpungeCLI/error_logs/errors.log'

def file_name(last_name, first_name, middle_name, birth_date, file_format):
    timestamp = datetime.today().strftime("%Y%m%d%H%M%S")

    filename = last_name + '_' + first_name
    if middle_name:
        filename += '_' + middle_name
    if birth_date:
        filename += '_' + birth_date.replace('/', '')
    filename += '_' + timestamp + file_format
    return filename

if PRODUCTION:
    print("Welcome :-)")
    url = 'https://morning-mountain-16534.herokuapp.com/error_logs'
    log_success = 'https://morning-mountain-16534.herokuapp.com/log_success'
    log_failure = 'https://morning-mountain-16534.herokuapp.com/log_failure'
else:
    url = 'http://localhost:3000/error_logs'
    log_success = 'http://localhost:3000/log_success'
    log_failure = 'http://localhost:3000/log_failure'

os.makedirs('Documents/RecordExpungeCLI/results', exist_ok=True)
os.makedirs('Documents/RecordExpungeCLI/error_logs', exist_ok=True)


crawler = Crawler()
username = input("Username: ")
password = getpass.getpass()

logged_in = crawler.login(username, password)

while not logged_in:
    print()
    print("Incorrect login information. Please re-enter credentials; otherwise hit control C to exit")
    print()
    username = input("Enter username: ")
    password = getpass.getpass()
    logged_in = crawler.login(username, password)

print()
print("Successfully logged in.")

while True:
    print("Please enter search parameters")
    print()

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")

    print()
    print("The next two parameters are optional. Hit enter if you wish to skip them")
    print()
    middle_name = input("Enter middle name: ")
    birth_date = input("Enter birth date: ")

    print()

    # Ensure log file is empty at start
    if os.path.isfile(ERROR_LOG_FILE):
        file = open(ERROR_LOG_FILE, mode='w')
        file.close()

    logging.basicConfig(filename=ERROR_LOG_FILE)

    print("Searching... and parsing results...")

    crawler.search(first_name, last_name, middle_name, birth_date)



    print("Search complete. Performing expungement")
    print()

    expunger = Expunger(crawler.result.cases)
    expunged = expunger.run()

    print("Expungement complete.")
    print()


    filename = file_name(last_name, first_name, middle_name, birth_date, '.txt')


    print("Creating file:", filename)

    dirfilename = 'Documents/RecordExpungeCLI/results/' + filename

    file = open(dirfilename, mode='x')

    print("Writing results to file...")

    num_charges_expungeable = 0
    expungeable_charges = []
    for case in expunger.cases:
        for charge in case.charges:
            if charge.expungement_result.type_eligibility and charge.expungement_result.time_eligibility:
                expungeable_charges.append(charge)
                num_charges_expungeable += 1

    total_balance_due = 0
    for case in expunger.cases:
        total_balance_due += case.balance_due_in_cents

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("Results for: " + last_name + ", " + first_name + "\n")
    file.write("\n\n")

    file.write("Number of cases  : " + str(len(expunger.cases)))
    file.write("\n")
    file.write("Number of charges: " + str(len(expunger._charges)))
    file.write("\n")
    file.write("Total balance due: $" + str(total_balance_due/100))
    file.write("\n")
    file.write("Total number of charges that can be expunged : " + str(num_charges_expungeable))
    file.write("\n\n")

    charge_count = 0

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            Expungeable charges\n")
    file.write("_________________________________________________________________________________________\n\n")
    for charge in expungeable_charges:
        file.write("  Case: " + charge.case()().case_number + "\n")
        file.write("      Charge     : " + charge.name + "\n")
        file.write("      Statute    : " + charge.statute + "\n")
        file.write("      Level      : " + charge.level + "\n")
        file.write("      Date       : " + str(charge.date) + "\n\n")
        file.write("      Disposition: '" + charge.disposition.ruling + "' : " + str(charge.disposition.date) + "\n\n")
        file.write("      Eligibility: \n\n")
        file.write("          Type eligible?  : " + str(charge.expungement_result.type_eligibility) + "\n")
        file.write("          Reason          : " + charge.expungement_result.type_eligibility_reason + "\n\n")
        file.write("          Time eligible?  : " + str(charge.expungement_result.time_eligibility) + "\n")
        file.write("          Reason          : " + charge.expungement_result.time_eligibility_reason + "\n\n")
        file.write("          Eligibility date: " + str(charge.expungement_result.date_of_eligibility) + "\n\n")
        file.write("     - - - - - - - - - - - - - - - - - - \n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            All Cases and Charges\n")
    for case in expunger.cases:
        file.write("_________________________________________________________________________________________\n\n")
        file.write("Case number : " + case.case_number + "\n")
        file.write("Case status : " + case.current_status + "\n")
        file.write("Case balance: $" + str(case.get_balance_due()) + "\n\n")
        charge_count = len(case.charges)

        for charge in case.charges:
            file.write("      Charge     : " + charge.name + "\n")
            file.write("      Statute    : " + charge.statute + "\n")
            file.write("      Level      : " + charge.level + "\n")
            file.write("      Date       : " + str(charge.date) + "\n\n")
            file.write("      Disposition: '" + charge.disposition.ruling + "' : " + str(charge.disposition.date) + "\n\n")
            file.write("      Eligibility: \n\n")
            file.write("          Type eligible?  : " + str(charge.expungement_result.type_eligibility) + "\n")
            file.write("          Reason          : " + charge.expungement_result.type_eligibility_reason + "\n\n")
            file.write("          Time eligible?  : " + str(charge.expungement_result.time_eligibility) + "\n")
            file.write("          Reason          : " + charge.expungement_result.time_eligibility_reason + "\n\n")
            file.write("          Eligibility date: " + str(charge.expungement_result.date_of_eligibility) + "\n\n")

            charge_count -= 1
            if charge_count > 0:
                file.write("     - - - - - - - - - - - - - - - - - - \n\n")

    print("Closing file")
    file.close()

    print()
    print("Checking error log...")
    print()

    with open(ERROR_LOG_FILE, 'r') as log_file:
        content = log_file.read()

    if content != '':
        print('*********************************************************')
        print('*************Sorry there were some Errors:***************')
        print('*********************************************************')
        print()
        for i in expunger.errors:
            print(f"    # {i}")
            print()


        print("Please wait: Uploading error log...")
        search_params = f"{last_name} : {first_name} : {middle_name} : {birth_date}"

        requests.post(log_failure)
        response = requests.post(url, data={'name': search_params, 'content': content})
        print()
        print('*********************************************************')
        if response.status_code > 399:
            print("There was an issue logging the error")
        else:
            print("Uploaded successfully.")
        print('*********************************************************')
        print()
    else:
        requests.post(log_success)
        print("No errors found.")
        print()

    print()
    if 'Open cases exist' in expunger.errors:
        print("Open cases exist: Time analysis was not done")

    answer = input("\nWould you like to do another search? (y/n): ")

    print(answer)
    if answer[0].lower() == 'y':
        crawler = Crawler()
        crawler.login(username, password)
    else:
        # erase log file by opening for writing and closing
        file = open(ERROR_LOG_FILE, mode='w')
        file.close()
        exit()
