\c record_expunge;

CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION citext;

CREATE FUNCTION CREATE_USER( email citext, admin boolean, hashed_password text) 
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

