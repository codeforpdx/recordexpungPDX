"""
All database ops on the Users and Auth tables
"""

from expungeservice.database.db_util import rollback_errors

@rollback_errors
def create_user(database, email, password_hash, admin):

    database.cursor.execute(
        """
        SELECT * FROM CREATE_USER( %(em)s, %(pass)s, %(adm)s );
        """, {'em':email, 'pass':password_hash, 'adm': admin})

    result = database.cursor.fetchone()
    database.connection.commit()
    return result._asdict()

def get_user_by_email(database, email):

    database.cursor.execute(
        """
            SELECT USERS.user_id::varchar, email, admin, hashed_password, auth_id::varchar
            FROM USERS JOIN AUTH ON USERS.user_id = AUTH.user_id
            WHERE email = %(em)s
        ;
        """, {"em":email}
        )
    res = database.cursor.fetchone()
    if res:
        return res._asdict()
    else:
        return res