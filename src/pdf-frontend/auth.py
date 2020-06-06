import getpass
from requests import Session


class Auth:
    @staticmethod
    def get_authenticated_client() -> Session:
        client = Session()

        oeci_logged_in = False
        while not oeci_logged_in:
            oeci_credentials = {
                "oeci_username": input("OECI username: "),
                "oeci_password": getpass.getpass("Password: "),
            }
            oeci_login_response = client.post("http://localhost:5000/api/oeci_login", json=oeci_credentials)
            if oeci_login_response.status_code == 201:
                oeci_logged_in = True
            else:
                print(oeci_login_response.text)
        return client
