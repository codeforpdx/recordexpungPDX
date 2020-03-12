CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS citext;

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

CREATE TABLE search_results (
    search_result_id      UUID NOT NULL,
    user_id               UUID REFERENCES users(user_id),
    date_searched         TIMESTAMP WITH TIME ZONE DEFAULT now(),
    hashed_search_params  TEXT NOT NULL,
    num_charges           INTEGER,
    num_eligible_charges  INTEGER,
    PRIMARY KEY (search_result_id)
);

