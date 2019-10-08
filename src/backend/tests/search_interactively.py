"""
An integration test script for running the expunger search using the flask test client.
Run the script in your environment with:

docker exec -ti expungeservice pipenv run python tests/search_interactively.py

"""

import expungeservice
import json
import getpass
import logging

logging.disable()



def flask_client_interactive_search():

    print("""\nOeci Record search.\n
Use this to log in to RecordExpunge and the OECI portal, \
then search and analyze records.\n""")

    app = expungeservice.create_app("development")
    client = app.test_client()

    logged_in = False
    while not logged_in:
        recordexpunge_credentials = {}
        recordexpunge_credentials["email"] = input("RecordExpunge email address: ")
        recordexpunge_credentials["password"] = getpass.getpass("password: ")

        auth_token_response = client.post(
        "/api/auth_token", json=recordexpunge_credentials)

        if auth_token_response.status_code == 200:
            logged_in = True
        else:
            print("Invalid login credentials.")
            continue

        auth_token = auth_token_response.get_json()["auth_token"]


    oeci_logged_in = False
    while not oeci_logged_in:

        oeci_credentials = {}

        oeci_credentials["oeci_username"] = input("OECI username: ")
        oeci_credentials["oeci_password"] = getpass.getpass("password: ")


        oeci_login_response = client.post(
            "/api/oeci_login",
            json=oeci_credentials,
            headers={"Authorization":"Bearer %s" % auth_token})
        if oeci_login_response.status_code == 201:
            oeci_logged_in = True
        else:
            print(oeci_login_response.status)

    done_searching = False
    print("===Record search===")
    while not done_searching:

        record_search_params = {}
        record_search_params["first_name"] = input("First name:")
        record_search_params["last_name"] = input("Last name:")
        record_search_params["middle_name"] = input("Middle name (can be blank):")
        record_search_params["birth_date"] = input("Birth date (format MM/DD/YYYY):")

        resp = client.post(
        "/api/search",
        json=record_search_params,
        headers={"Authorization":"Bearer %s" % auth_token})

        record = resp.get_json()["data"]["record"]

        print("\n======\n" + json.dumps(record, indent=4) + "\n\n")

        answered = False
        while not answered:
            repeat = input("Search again? (y/n) ").strip().lower()
            if repeat == "y":
                answered = True
            elif repeat == "n":
                answered = True
                done_searching = True

"""
To run the login and search without needing to type interactively, you can
use this function and provide the data required for the three endpoint calls:

auth_token:
 - "email"
 - "password"

oeci_login:
 - "oeci_username"
 - "oeci_password"

search:
 - "first_name"
 - "last_name"
 - "middle_name"
 - "birth_date"

"""

def flask_client_oeci_search(
    recordexpunge_credentials,
    oeci_credentials,
    record_search_params):

    app = expungeservice.create_app("development")
    client = app.test_client()


    auth_token_response = client.post(
        "/api/auth_token", json=recordexpunge_credentials)

    auth_token = auth_token_response.get_json()["auth_token"]

    oeci_login_response = client.post(
        "/api/oeci_login",
        json=oeci_credentials,
        headers={"Authorization":"Bearer %s" % auth_token})
    # Nothing to extract from the oeci response object; it just attaches a cookie to the client

    resp = client.post(
        "/api/search",
        json=record_search_params,
        headers={"Authorization":"Bearer %s" % auth_token})

    record = resp.get_json()["data"]["record"]

    return record


if __name__ == "__main__":
    flask_client_interactive_search()