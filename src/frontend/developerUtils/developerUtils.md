## Mocking OECI endpoints

These files help mock out the interaction with the backend for OECI authentication and requesting search results.

With these you will be able to receive mocked record search results if you are properly authenticated.

The OECI log in information:
> User ID: username
> Password: password

To make a search request using the mocked endpoint you do not need specific first name, last name, or date of birth at this point. Currently we are returning static JSON based on a successful OECI authenticated request.

Run the alternate version of the app by running the make target in the project root:

`$ make dev_mock_oeci_up`

This uses a docker volume mapping to replace the regular oeci endpoint files with the mocked versions within the running container.

Stop the app with the usual make target:

`$ make dev_down`