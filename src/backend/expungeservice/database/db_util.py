
import functools

def rollback_errors(db_operation):
    @functools.wraps(db_operation)
    def wrapper(database, *args, **kwargs):
        
        try:
            return db_operation(database, *args, **kwargs)
        except Exception as ex:
            database.connection.rollback()
            raise ex
        
    return wrapper