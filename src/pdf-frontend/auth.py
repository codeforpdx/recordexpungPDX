import getpass
from requests import Session


class Auth:
    @staticmethod
    def get_authenticated_client() -> Session:
        client = Session()

        logged_in = False
        while not logged_in:
            credentials = {}
            credentials["email"] = input("RecordSponge email address: ")
            credentials["password"] = getpass.getpass("Password: ")

            auth_token_response = client.post("http://localhost:5000/api/auth_token", json=credentials)

            if auth_token_response.status_code == 200:
                logged_in = True
            else:
                print("Invalid login credentials.")
                continue

        oeci_logged_in = False
        while not oeci_logged_in:
            oeci_credentials = {
                "oeci_username": input("OECI email address: "),
                "oeci_password": getpass.getpass("Password: "),
            }
            if not oeci_credentials:
                oeci_credentials["oeci_username"] = input("OECI username: ")
                oeci_credentials["oeci_password"] = input("Password: ")

            oeci_login_response = client.post("http://localhost:5000/api/oeci_login", json=oeci_credentials)
            if oeci_login_response.status_code == 201:
                oeci_logged_in = True
            else:
                print(oeci_login_response.text)
        return client
