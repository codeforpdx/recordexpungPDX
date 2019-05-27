\c record_expunge;

CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION citext;

CREATE TABLE users (
    user_id         UUID NOT NULL,
    email           CITEXT UNIQUE NOT NULL,
    admin           BOOLEAN NOT NULL DEFAULT FALSE,
    date_created    TIMESTAMP WITH TIME ZONE DEFAULT now(),
    date_modified   TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (user_id)
);

CREATE TABLE auth (
    auth_id         UUID NOT NULL,
    hashed_password TEXT NOT NULL,
    user_id        UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (auth_id)
);


CREATE TABLE clients (
    client_id     UUID NOT NULL,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    date_created  TIMESTAMP WITH TIME ZONE DEFAULT now(),
    date_modified TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (client_id),
    UNIQUE (first_name, last_name, date_of_birth)
);


CREATE TABLE result_codes (
    result_code_id UUID NOT NULL,
    code           TEXT UNIQUE NOT NULL,
    PRIMARY KEY (result_code_id)
);


CREATE TABLE rules (
    rule_id UUID NOT NULL,
    text    TEXT UNIQUE NOT NULL,
    PRIMARY KEY (rule_id)
);


CREATE TABLE analyses (
    client_id UUID NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
    case_id   TEXT NOT NULL,
    result_code_id UUID NOT NULL REFERENCES result_codes(result_code_id) ON DELETE CASCADE,
    statute        TEXT NOT NULL,
    date_eligible  TIMESTAMP WITH TIME ZONE,
    rule_ids       UUID[] NOT NULL,
    date_created   TIMESTAMP WITH TIME ZONE DEFAULT now(),
    date_modified  TIMESTAMP WITH TIME ZONE DEFAULT now(),
    expunged       BOOLEAN,
    date_expunged  TIMESTAMP WITH TIME ZONE,
    user_id        UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (client_id, case_id)
);


CREATE FUNCTION public.CREATE_USER( email citext, admin boolean, hashed_password text) 
RETURNS TABLE (USER_ID VARCHAR, EMAIL CITEXT, ADMIN BOOLEAN, AUTH_ID VARCHAR, HASHED_PASSWORD TEXT)
as $$
WITH USER_INSERT_RESULT AS 
            (
            INSERT INTO USERS (user_id, email, admin)
            VALUES ( uuid_generate_v4(), $1, $2)
            RETURNING user_id)
            INSERT INTO AUTH (auth_id, hashed_password, user_id)
            SELECT uuid_generate_v4(), $3, user_id FROM USER_INSERT_RESULT;
            
SELECT USERS.USER_ID::varchar, EMAIL, ADMIN, AUTH_ID::varchar, HASHED_PASSWORD 
FROM USERS JOIN AUTH ON USERS.USER_ID = AUTH.USER_ID 
WHERE EMAIL=$1;
$$
LANGUAGE SQL;

