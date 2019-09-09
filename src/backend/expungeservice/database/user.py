"""
All database ops on the Users and Auth tables
"""

from expungeservice.database.db_util import rollback_errors

from psycopg2 import sql

@rollback_errors
def create_user(database, email, name,
        group_name, password_hash, admin):

    database.cursor.execute(
        """
        SELECT * FROM CREATE_USER( %(em)s, %(pass)s, %(name)s, %(group_name)s, %(adm)s );
        """, {'em':email, 'pass':password_hash, 'name':name,
              'group_name':group_name,
              'adm': admin})

    result = database.cursor.fetchone()
    database.connection.commit()
    return result._asdict()

def get_user_by_id(database, user_id):

    return get_user(database, lookup_field = "user_id", key = user_id)

def get_user_by_email(database, email):

    return get_user(database, lookup_field = "email", key = email)


def get_user(database, lookup_field, key):

    database.cursor.execute(
        sql.SQL("""
            SELECT USERS.user_id::text user_id, email, admin,
            hashed_password, auth_id::text, date_created, date_modified
            FROM USERS JOIN AUTH ON USERS.user_id = AUTH.user_id
            WHERE users.{} = %(key)s
        ;
        """).format(sql.Identifier(lookup_field)), {"key":key}
        )

    res = database.cursor.fetchone()
    if res:
        return res._asdict()
    else:
        return res


def get_all_users(database):

    database.cursor.execute(
        sql.SQL("""

            SELECT USERS.user_id::text user_id, email, name, group_name, admin, hashed_password, auth_id::text, date_created, date_modified
            FROM USERS JOIN AUTH ON USERS.user_id = AUTH.user_id
        ;
        """), {})

    res = database.cursor.fetchall()
    if res:
        return [r._asdict() for r in res]
    else:
        return res

