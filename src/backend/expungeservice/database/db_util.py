import functools
import json
from flask import g
import uuid
import hashlib
from flask_login import current_user


def rollback_errors(db_operation):
    @functools.wraps(db_operation)
    def wrapper(database, *args, **kwargs):

        try:
            return db_operation(database, *args, **kwargs)
        except Exception as ex:
            database.connection.rollback()
            raise ex

    return wrapper


def save_search_event(aliases_data):
    user_id = current_user.user_id
    search_param_string = user_id + json.dumps(aliases_data, sort_keys=True)
    hashed_search_params = hashlib.sha256(search_param_string.encode()).hexdigest()
    _db_insert_search_event(g.database, user_id, hashed_search_params)


@rollback_errors
def _db_insert_search_event(database, user_id, hashed_search_params):
    database.cursor.execute(
        """
        INSERT INTO  SEARCH_RESULTS(search_result_id, user_id, hashed_search_params)
        VALUES ( uuid_generate_v4(), %(user_id)s, %(params)s);
        """,
        {"user_id": uuid.UUID(user_id).hex, "params": hashed_search_params,},
    )
