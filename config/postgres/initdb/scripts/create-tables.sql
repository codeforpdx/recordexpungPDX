CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION citext;

CREATE TABLE users (
    user_id         UUID NOT NULL,
    email           CITEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    group_name      TEXT,
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
