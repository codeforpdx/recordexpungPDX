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
- [Database Schema](#database)
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

These endpoints comprise our API. All requests of these endpoints go through the web server.


Global headers:

- `Content-Type: application/json`
- `Accept: application/json`


**`POST`** `/api/auth_token`

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
    * user_id
    * auth_token


 Status codes:

- `201 CREATED`: auth token creation successful
- `401 UNAUTHORIZED`: unable to create auth token: invalid email / password
- `400 BAD FORMAT`: missing email or password


**`GET`** `/api/users/`

Fetches the list of existing users. requires admin authorization

Required headers:

- `Authorization: <JWT auth_token>`

Returns: List of users:

- format: `JSON`
- fields:
    * users :: list
        * user_id
        * email
        * name
        * group
        * admin
        * date_created_timestamp

Status codes:

- `200 OK`
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin


**`GET`** `/api/user/user_id`

Required headers:

- `Authorization: <JWT auth_token>`

Returns: Requested user. requires admin authorization or that the logged-in user match the requested user_id.

- format: `JSON`
- fields:
    * user_id
    * email
    * name
    * group
    * admin
    * timestamp
    

Status codes:

- `200 OK`
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin or doesn't match the requested user_id 


**`POST`** `/api/user/`

Creates a user

Required headers:

- `Authorization: <JWT string>`

`POST` body:

- format: `JSON`
- fields:
    * email
    * name
    * group
    * password
    * admin

Returns: New user

- format: `JSON`
- fields:
    * user_id
    * email
    * name
    * group
    * admin
    * timestamp


Status codes:

- `201 CREATED`: user creation was successful
- `400 BAD FORMAT`: missing one or more fields
- `401 UNAUTHORIZED`: authorization rejected; missing or invalid auth token
- `403 FORBIDDEN`: authorized user is not admin
- `422 UPROCESSABLE ENTITY`: duplicate user or password too short



**`GET`** `/api/search`

Performs search of remote system

Required headers:

- `Authorization: <JWT auth_token>`

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


**`GET`** `/api/stats`

Reports on statistics run on data

Returns:

- format: `JSON`
- fields:
    * tbd


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

    users (uuid, email, admin, date_created, date_modified), uuid primary key

    auth (uuid, hashed_password, user_id), uuid primary key

    result_codes (uuid, code) uuid primary key

    rules (uuid, text)


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
