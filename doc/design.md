Record Expunge System
=====================

Some thoughts on the Record Expunge System.


Stack
-----

[ Web Server ]  -- Apache or Nginx, https enabled

[ Application ] -- JavaScript/ReactJS

[ Micro Service ] [ Database ] -- Python, Flask, Requests, PostgreSQL, Psycopg, Swagger


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


Application Routes
------------------

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


Back-End Endpoints
------------------

These endpoints comprise our API. All requests of these endpoints go through the web server.


Global headers:

- `Content-Type: application/json`
- `Accept: application/json`


**`POST`** `/api/<version>/auth_token`

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


**`POST`** `/api/<version>/users/`

Creates a user

`POST` body:

- format: `JSON`
- fields:
    * email
    * encrypted password
    * admin permissions

Returns: New user

- format: `JSON`
- fields:
    * email
    * admin permissions
    * timestamp

Status codes:

- `201 CREATED`: user creation was successful
- `401 UNAUTHORIZED`: user creation was not succesful: user not found
- `400 BAD FORMAT`: missing one or more fields


**`GET`** `/api/<version>/users/EMAIL`

Returns: Requested user

- format: `JSON`
- fields:
    * email
    * admin permissions
    * timestamp

Status codes:

- `200 OK`


**`POST`** `/api/<version>/search`

Performs search of remote system

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


**`GET`** `/api/<version>/stats`

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

    clients (uuid, first_name, last_name, dob, date_created, date_modified), uuid primary key

    result_codes (uuid, code) uuid primary key

    rules (uuid, text)

    analyses (client_id, case_id, result_code, statute, date_eligible, rules[], date_created, date_modified, expunged, date_expunged)


Notes:

- Store passwords encrypted
- Use Postgres features for exporting JSON
