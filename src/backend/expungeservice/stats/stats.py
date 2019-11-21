from flask import g
import uuid

from expungeservice.database.db_util import rollback_errors
from expungeservice.models.expungement_result import EligibilityStatus


def save_result(user_id, request_data, record):

    hashed_search_params = hash(
        user_id +
        request_data["first_name"] +
        request_data["last_name"] +
        request_data["middle_name"] +
        request_data["birth_date"])

    num_charges = len(record.charges)

    num_eligible_charges = len([ c for c in record.charges if
        c.expungement_result.type_eligibility.status == EligibilityStatus.ELIGIBLE])

    insert_result = db_insert_result(
        g.database, user_id, hashed_search_params, num_charges, num_eligible_charges)


@rollback_errors
def db_insert_result(database, user_id, hashed_search_params, num_charges, num_eligible_charges):

    result= database.cursor.execute(
        """
        INSERT INTO  SEARCH_RESULTS(search_result_id, user_id, hashed_search_params, num_charges, num_eligible_charges )
        VALUES ( uuid_generate_v4(), %(user_id)s, %(params)s, %(num_charges)s, %(num_eligible_charges)s);
        """, {'user_id': uuid.UUID(user_id).hex, 'params': hashed_search_params, 'num_charges': num_charges,
              'num_eligible_charges': num_eligible_charges})
