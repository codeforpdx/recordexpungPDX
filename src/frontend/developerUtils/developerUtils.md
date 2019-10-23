These files help mock out the interaction with the backend for OECI authentication and requesting search results.   

With these you will be able to recieve mocked record search results if you are properly authenticated.

The OECI log in information:  
> User ID: username  
> Password: password  

To make a search request you do not need specific first name, last name, or date of birth at this point. Currently we are returning static JSON based on a successful OECI authenticated request.  

To use them replace the corresponding files in the `/src/backend/expungeservice/endpoints/...` folder.  

## IMPORTANT! Do not check these modified files into version control. They should only be used to help build out the remaining frontend components for the search results.  

from the root directory of the app you can run:  

`cp src/frontend/developerUtils/search.py src/backend/expungeservice/endpoints/search.py`  

`cp src/frontend/developerUtils/oeci_login.py src/backend/expungeservice/endpoints/oeci_login.py`  

## Before committing make sure to revert these two files to their original forms.  