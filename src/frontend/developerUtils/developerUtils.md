## Mocking OECI endpoints

These files help mock out the interaction with the backend for OECI authentication and requesting search results. With these you will be able to receive mocked record search results from /api/search after getting a mocked authentation cooking from /api/oeci_login.

The purpose here is to allow testing for frontend/backend integration without the backend making actual requests to the OECI site.

Valid credentials for the OECI mocked endpoint are:

> User ID: username
> Password: password

To make a search request using the mocked endpoint you do not need specific first name, last name, or date of birth at this point. Currently the endpoint returns static JSON, so long as the client has already obtained the oeci authentication cookie.

Run the alternate version of the app by running the make target in the project root:

`$ make dev_mock_oeci_up`

This uses a docker volume mapping to replace the regular oeci endpoint files with the mocked versions within the running container.

Stop the app with the usual make target:

`$ make dev_down`

### Note:

If the oeci source files in `src/backend/endpoints/` are changed, these mock versions may need to be updated as well or the utility will break.