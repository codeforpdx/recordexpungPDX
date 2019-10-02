import os
import getpass
import requests
import logging
import threading

from src.backend.expungeservice.crawler.crawler import Crawler
from src.backend.expungeservice.expunger.expunger import Expunger
from datetime import datetime


##############################################
VERSION = 'v0.3.3'
PRODUCTION = True
##############################################

ERROR_LOG_FILE = 'Documents/RecordExpungeCLI/error_logs/errors.log'

def has_eligible_charge(case):
    for el in case.charges:
        if el.expungement_result.type_eligibility is True and el.expungement_result.time_eligibility is True:
           return True
    return False

def has_future_eligible_charge(case):
    for el in case.charges:
        return el.expungement_result.type_eligibility is True and not el.expungement_result.time_eligibility

def get_eligibility_date(case):
    for el in case.charges:
        if el.expungement_result.type_eligibility is True:
            return str(el.expungement_result.date_of_eligibility)

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
    home_url = 'https://morning-mountain-16534.herokuapp.com'
    url = 'https://morning-mountain-16534.herokuapp.com/error_logs'
    log_success = 'https://morning-mountain-16534.herokuapp.com/log_success'
    log_failure = 'https://morning-mountain-16534.herokuapp.com/log_failure'
else:
    print("Loading development environment")
    home_url = 'http://localhost:3000'
    url = 'http://localhost:3000/error_logs'
    log_success = 'http://localhost:3000/log_success'
    log_failure = 'http://localhost:3000/log_failure'

def ping_server():
    try:
        # wake up logging server
        requests.get(home_url)
    except Exception:
        pass

logging_server = threading.Thread(target=ping_server)
logging_server.start()

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

    print("Pinging logging server to wake it up...")
    ping_server()

    print()

    print("Searching... and parsing results...")

    record = crawler.search(first_name, last_name, middle_name, birth_date)



    print("Search complete. Performing expungement")
    print()

    expunger = Expunger(record)
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
    for case in record.cases:
        for charge in case.charges:
            if charge.expungement_result.type_eligibility and charge.expungement_result.time_eligibility:
                expungeable_charges.append(charge)
                num_charges_expungeable += 1

    total_balance_due = 0
    for case in record.cases:
        total_balance_due += case.balance_due_in_cents

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("Results for: " + last_name + ", " + first_name + "\n")
    file.write("\n\n")

    file.write("Number of cases  : " + str(len(record.cases)))
    file.write("\n")
    file.write("Number of charges: " + str(len(record.charges)))
    file.write("\n")
    file.write("Total balance due: $" + str(total_balance_due/100))
    file.write("\n")
    file.write("Total number of charges that can be expunged : " + str(num_charges_expungeable))
    file.write("\n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            Expungeable Cases\n")
    file.write("_________________________________________________________________________________________\n\n")

    for case in record.cases:
        if has_eligible_charge(case):
            file.write(case.case_number + " : " + case.violation_type)
            file.write("\n")

    file.write("\n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            Future: Expungeable Cases\n")
    file.write("_________________________________________________________________________________________\n\n")

    for case in record.cases:
        if has_future_eligible_charge(case):
            file.write(case.case_number + " : " + case.violation_type + " | Eligibility Date: " + get_eligibility_date(case))
            file.write("\n")

    file.write("\n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            Further Analysis needed\n")
    file.write("_________________________________________________________________________________________\n\n")
    for case in record.cases:
        for charge in case.charges:
            if charge.expungement_result.type_eligibility is None:
                file.write("  Case: " + charge.case()().case_number + "\n")

    file.write("\n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                            Expungeable charges\n")
    file.write("_________________________________________________________________________________________\n\n")

    charge_count = 0
    for charge in expungeable_charges:
        file.write("  Case: " + charge.case()().case_number + "\n")
        file.write("\n")
        file.write("     " + charge.__class__.__name__ + "\n\n")
        file.write("      Charge     : " + charge.name + "\n")
        file.write("      Statute    : " + charge.statute + "\n")
        file.write("      Level      : " + charge.level + "\n")
        file.write("      Date       : " + str(charge.date) + "\n\n")
        if charge.disposition:
            file.write("      Disposition: '" + charge.disposition.ruling + "' : " + str(charge.disposition.date) + "\n\n")
        else:
            file.write("      Disposition: None")
        file.write("      Eligibility: \n\n")
        file.write("          Type eligible?  : " + str(charge.expungement_result.type_eligibility) + "\n")
        file.write("          Reason          : " + charge.expungement_result.type_eligibility_reason + "\n\n")
        file.write("          Time eligible?  : " + str(charge.expungement_result.time_eligibility) + "\n")
        file.write("          Reason          : " + charge.expungement_result.time_eligibility_reason + "\n\n")
        file.write("          Eligibility date: " + str(charge.expungement_result.date_of_eligibility) + "\n\n")
        file.write("     - - - - - - - - - - - - - - - - - - \n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("                     All Cases and Charges (Excluding most Parking tickets)\n")
    for case in record.cases:
        if not 'parking' in case.violation_type.lower():
            file.write("_________________________________________________________________________________________\n\n")
            file.write("Case number : " + case.case_number + "\n")
            file.write("Case status : " + case.current_status + "\n")
            file.write("Case balance: $" + str(case.get_balance_due()) + "\n\n")
            charge_count = len(case.charges)

            for charge in case.charges:
                file.write("     " + charge.__class__.__name__ + "\n\n")
                file.write("      Charge     : " + charge.name + "\n")
                file.write("      Statute    : " + charge.statute + "\n")
                file.write("      Level      : " + charge.level + "\n")
                file.write("      Date       : " + str(charge.date) + "\n\n")
                if charge.disposition:
                    file.write("      Disposition: '" + charge.disposition.ruling + "' : " + str(charge.disposition.date) + "\n\n")
                else:
                    file.write("      Disposition: None")
                file.write("      Eligibility: \n\n")
                file.write("          Type eligible?  : " + str(charge.expungement_result.type_eligibility) + "\n")
                file.write("          Reason          : " + charge.expungement_result.type_eligibility_reason + "\n\n")
                file.write("          Time eligible?  : " + str(charge.expungement_result.time_eligibility) + "\n")
                file.write("          Reason          : " + charge.expungement_result.time_eligibility_reason + "\n\n")
                file.write("          Eligibility date: " + str(charge.expungement_result.date_of_eligibility) + "\n\n")

                charge_count -= 1
                if charge_count > 0:
                    file.write("     - - - - - - - - - - - - - - - - - - \n\n")

    file.write("-----------------------------------------------------------------------------------------\n")
    file.write("-----------------------------------END OF FILE-------------------------------------------\n")
    file.write("-----------------------------------------------------------------------------------------\n")

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

        try:
            requests.post(log_failure, data={'version': VERSION})
            response = requests.post(url, data={'name': search_params, 'content': content})
        except Exception:
            pass
        print()
        print('*********************************************************')
        if response.status_code > 399:
            print("There was an issue logging the error")
        else:
            print("Uploaded successfully.")
        print('*********************************************************')
        print()
    else:
        try:
            requests.post(log_success, data={'version': VERSION})
        except Exception:
            pass
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
