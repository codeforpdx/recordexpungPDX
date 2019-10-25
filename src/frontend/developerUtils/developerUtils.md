## IMPORTANT! Do not check the modified files into version control.

These files help mock out the interaction with the backend for OECI authentication and requesting search results.   

With these you will be able to recieve mocked record search results if you are properly authenticated.

The OECI log in information:  
> User ID: username  
> Password: password  

To make a search request you do not need specific first name, last name, or date of birth at this point. Currently we are returning static JSON based on a successful OECI authenticated request.  

To use them replace the corresponding files in the `/src/backend/expungeservice/endpoints/...` folder.  

from the root directory of the app you can run:  

`$ make dev_utils_up`

## Before committing make sure to revert these two files to their original forms.  

`$ make dev_utils_down`