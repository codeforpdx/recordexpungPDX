Record Expunge System
=====================

Some thoughts on the Record Expunge System.


Table of Contents
-----------------
- [Project Stack](#project-stack)
- [User Flow](#user-flow)
- [Frontend Routes](#frontend-routes)
- [Backend Endpoints](#backend-endpoints)
- [Data Model](#data-model)
- [Database Schema](#database-schema)
- [Database Functions](#database-functions)

- [License](#license)

Project Stack
-------------

The app stack is deployed as three services in a Docker stack:

[ Web Server ]  -- Nginx, https enabled. Serves static pages and proxies API calls

[ Backend API ] -- Python, Flask, Psycopg

[ Database ] -- PostgreSQL


User Flow
---------

User visits login page in browser

User types email and password to log in

User is directed to main page

User has option to search, view stats, or log out

If user chooses search:

- User enters search terms

- Service logs into remote site

- Service does search on remote site

- Remote site returns HTML page of results

- Service scrapes results

- Service parses scraped results

- Service makes decision based on Expunge Rules

- Service inserts records into database

- User is directed to page of pretty-fied scraped results

- User has option to search again, view stats, or log out


If user chooses stats:

- User is directed to stats page showing XYZ statistics


If user chooses log out:

- User is logged out of system
    * Session cookie is invalidated

- User is directed to login page


Frontend Routes
---------------

These routes are set up in the front-end application for navigating between the different views.

`/login`

Login page

- Form for entering `email` and `password`
- Application sends credentials to server
- Server validates credentials
- If credentials are good server returns session cookie (contents tbd)
- If credentails are not good server returns `401` or `422`

`/main`

Main page

- Search: search remote system
- Stats: view statistics of data
- Log out: log out of system


`/search`

Search page

- Form for entering first name, last name, dob
- Shows results of search

`/stats`

Page for viewing statistics


`/admin`

Admin page for creating users

- email
- password
- admin permissions (T/F)


Backend Endpoints
-----------------

These endpoints comprise our API. All requests of these endpoints go through the frontend web server and get routed to the backend server with the nginx reverse-proxy.


Global headers:

- `Content-Type: application/json`
- `Accept: application/json`


### **`POST`** `/api/auth_token`

Post email, password to create an auth token (JWT) that can be used when
accessing protected APIs

`POST` body:

- format: `JSON`
- fields:
    * `email`
    * `password`

Returns: auth token

- format: `JSON`
- fields:
    * auth_token

 Status codes:

- `201 CREATED`: auth token creation successful
- `401 UNAUTHORIZED`: unable to create auth token: invalid email / password
- `400 BAD FORMAT`: missing email or password


### **`GET`** `/api/users/`

Fetches the list of existing users

Required headers:

- `Authorization: <JWT string>`

Returns: List of users:

- format: `JSON`
- fields:
    * users :: list
        * email
        * admin
        * timestamp

Status codes:

- `200 OK`
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin


### **`GET`** `/api/user?email=EMAIL`

Fetches the data for a single user. Admin access is required if the requested email does not match the logged-in user (identified by the JWT token)

## Question

What is this used for in the frontend? An admin inspecting a single user's profile?
Any user inspecting their own profile?
What data should be returned? Is it different for those two use cases?


Required headers:

- `Authorization: <JWT string>`

Returns: Requested user

- format: `JSON`
- fields:
    * email
    * admin
    * timestamp
    * name
    * group

Status codes:

- `200 OK`
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin or doesn't match the requested user

- `404 NOT FOUND`

## Question:

Is 404 still appropriate if it's due to a query param and not a path?
Or is this a  `422 UPROCESSABLE ENTITY` as though it was a field in POST body?


### **`POST`** `/api/new_user/`

Creates a user and sends a verification email with a link to set a password.

Required Headers:
- `Authorization: <JWT string>`

`POST` body:

- format: `JSON`
- fields:
    * email
    * admin
    * name
    * group

Returns: New user

- format: `JSON`
- fields:
    * email
    * admin
    * created_timestamp
    * name
    * group


Note:
- user_id is not required by the frontend here so is not returned.

Status codes:

- `201 CREATED`: user creation was successful
- `400 BAD FORMAT`: missing one or more fields
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin
- `422 UPROCESSABLE ENTITY`: duplicate user or password too short


### **`POST`** `/api/search`

Performs search of remote OECI system.

## Question

We need to design the workflow for logging into OECI. See Question below at **`POST`** `/oeci_login/`

`POST` body:

- format: `JSON`
- fields:
    * first name
    * last name
    * dob

Returns: Search results

- format: `JSON`
- fields:
    * tbd


### **`GET`** `/api/stats`

Reports on statistics run on data

Returns:

- format: `JSON`
- fields:
    * tbd


### **`POST`** `/oeci_login` ?

## Question

What's the workflow for accessing OECI?

Is it a webpage redirect, like the frontend prototype?

Or is it an authentication serverside, like the current Crawler implementation?
These behaviors need to be reconciled.

I see three design versions:

- Rely on a frontend page redirect, which obtains login access from the OECI directly to allow subsequent requests by Crawler. This requires a Crawler redesign, which currently passes creds to the remote site. It also requires caching a login token provided by OECI. Does the OECI login allow that, e.g. use a cookie?

- Roll the login  into the `/search/` endpoint.
If so, we need to add oeci credentials to the **`POST`** `/search/ ` body. And also cache the login credentials clientside so we can re-send them on every search (bad).

- Send oeci login credentials to the backend once, and the /search/ endpoint uses them for every /search/ call. That means caching the OECI login creds in the backend.



### **`POST`** `/api/forgot_password`

Requests a password reset link be sent to a valid (recognized) email address

`POST` body:

- format: `JSON`
- fields:
    * email

Status codes:

- `200 OK`
- `422 UPROCESSABLE ENTITY` email not recognized
- `5xx` of some kind if the email-send failed


### **`POST`** `/api/update_password`

Follows a password reset link (from a sent email), that provides login authorization

## Question: How does this work?

A password reset link provided in an email needs to be a GET request, so the endpoint requires a different method for yielding auth access. If this method is a POST and auth-protected, we need to first obtain an auth_token via the **`GET`** `/api/auth_token` method below.

### Or,

Is this a GET that has been passed an `auth_token` string as a url query param? That's an irregular authorization that is not processed in a POST header, but we're still using it to authorize a password-change. that's weird. I like option 1 better.


Headers:
- `Authorization: <JWT_AUTH_TOKEN>`

`POST` body:

- format: `JSON`
- fields:
    * email

Status codes:

- `200 OK`
- `422 UPROCESSABLE ENTITY`


### **`GET`** `/api/auth_token?auth=<special_auth_token>`

Obtains an auth_token using a query param instead of login credentials.
This is necessary for one option of the Password Reset workflow described above.

Status codes:

- `200 OK`
- `422 UPROCESSABLE ENTITY` if the auth token query param is invalid

Returns: auth token usable as a regular POST Authorization header.

- format: `JSON`
- fields:
    * auth_token
    
### **`POST`** `/api/change_user_settings`

Alter user account settings, like password, email address, and admin access, or account information like Name or Group

## Comment re password-reset

If the workflow to change your password is: 1) obtain a regular JWT token by special means (without password) then 2) use your new JWT token to change your password, then this endpoint can just be used to change your password. That sounds DRY. 

Headers:
- `Authorization: <JWT_AUTH_TOKEN>`

- format: `JSON`
- fields:
    * email
    * new_email [optional]
    * new_name [optional]
    * new_group [optional]
    * new_password [optional]
    * new_admin_value [optional]

    Status codes:

- `200 OK`
- `422 UPROCESSABLE ENTITY`
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is admin but is trying to change password
- `403 FORBIDDEN`: authorized user is not admin nor the target user





Data Model
----------

#### Record:
 - cases :: type list[Case]

#### Case:
 - name
 - birth_year
 - case_number
 - citation_number
 - date
 - location
 - violation_type
 - current_status
 - balance_due_in_cents
 - case_detail_link
 - charges # type list[Charge]

#### Charge:
 - name
 - statute
 - level
 - date
 - disposition :: type list[Disposition]
 - expungement_result :: type ExpungementResult

#### Disposition:
 - date
 - ruling

#### ExpungementResult:
 - type_eligibility
 - type_eligibility_reason
 - time_eligibility
 - time_eligibility_reason
 - date_of_eligibility


Database Schema
---------------

Tables:

    users (uuid, email, name, group, admin, date_created, date_modified, activated), uuid primary key

    auth (uuid, hashed_password, user_id), uuid primary key

    result_codes (uuid, code) uuid primary key

    rules (uuid, text)

## Question:

Do we store client information? I think we have at some point decided not to. 

    clients (uuid, first_name, last_name, dob, date_created, date_modified), uuid primary key

    analyses (client_id, case_id, result_code, statute, date_eligible, rules[], date_created, 
    date_modified, expunged, date_expunged)


Notes:

- Store passwords encrypted
- Use Postgres features for exporting JSON

Database Functions
--------------
Functions that query or update the database will be organized into a single module in the expungeservice.

    create_user(database, email, admin, hashed_password)

Insert a new user into the Users table with the given email string and admin flag, and inserts the password hash into the Auth table and link it with the User uuid. The uuid of each, and the date_created and date_updated are generated within the database.

This pair of inserts is an atomic operation, so if one fails then the other one is cancelled and has no effect.
If successful, returns an OrderedDictionary object containing the created entry. Otherwise throws the relevant error.

    get_user_by_email(database, email)

Return the user data identified by the given email string, in OrderedDictionary format. Contains the email string, hashed_password, admin flag, and the UUIDs for user and auth. If no such user exists, returns None. Throw any errors generated by the database.

    save_stats(database, email, record)

Takes a Record object which has processed by the expungement analyzer. Saves only a limited amount of information. Details tbd, but here are a few examples for tracking app usage and app impact:
 -  User activity: When a search is performed, log the username and timestamp; but not the search parameters.
  - Expunged charges: record the individual charges, by their crime level, some eligibility information, and the month that the search was performed.
     * An inexact timestamp makes it hard to reconstruct a complete record which could then be de-anonymized.
     * Eligibility information could be kept vague, e.g, only "eligible", "not eligible", "time-eligible", and "undetermined", as opposed to keeping the detailed analysis returned by the expunger.
