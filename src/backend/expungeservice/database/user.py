"""
All database ops on the Users and Auth tables
"""

from expungeservice.database.db_util import rollback_errors

from psycopg2 import sql


@rollback_errors
def create(database, email, name,
           group_name, password_hash, admin):

    database.cursor.execute(
        """
        SELECT * FROM USERS_CREATE( %(em)s, %(pass)s, %(name)s, %(group_name)s,
         %(adm)s );
        """, {'em': email, 'pass': password_hash, 'name': name,
              'group_name': group_name,
              'adm': admin})

    result = database.cursor.fetchone()
    return result._asdict()


def identify_by_email(database, email):
    database.cursor.execute(
        """
        SELECT user_id::text
        FROM USERS where email = %(email)s
        ;""", {"email": email})

    res = database.cursor.fetchone()
    if res:
        return res._asdict()['user_id']
    else:
        return None


def read(database, user_id):

    database.cursor.execute(

        """
        SELECT * FROM USERS_READ( %(user_id)s );
        """, {'user_id': user_id})

    res = database.cursor.fetchone()

    if res:
        return res._asdict()
    else:
        return None


def fetchall(database):

    database.cursor.execute(
        sql.SQL(
            """SELECT * FROM USERS_FETCHALL();
            """), {})

    res = database.cursor.fetchall()
    if res:
        return [r._asdict() for r in res]
    else:
        return None


@rollback_errors
def update(database, user_id, new_values):

    user_data = read(database, user_id)
    if not user_data:
        return None

    for col_name in ["name", "email", "group_name", "admin", "hashed_password"]:
        if col_name in new_values.keys():
            user_data[col_name] = new_values[col_name]
    user_data["user_id"] = user_id

    database.cursor.execute(
        """SELECT * FROM USERS_UPDATE(
            %(user_id)s, %(email)s,  %(name)s, %(group_name)s,
            %(admin)s, %(hashed_password)s )""",
        user_data)

    res = database.cursor.fetchone()

    if res:
        return res._asdict()
    else:
        return None


'''
Here is an example of safe SQL formatting to insert column names and values:

lookup_field = "email"
key = "person@email.com"
database.cursor.execute(
        sql.SQL("""
            SELECT USERS.user_id::text user_id, email, hashed_password
            FROM USERS JOIN AUTH ON USERS.user_id = AUTH.user_id
            WHERE users.{} = %(key)s
            ;
            """).format(sql.Identifier(lookup_field)), {"key":key}
        )
'''
