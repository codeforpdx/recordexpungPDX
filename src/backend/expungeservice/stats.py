import json

from flask import g
import uuid
import hashlib

from expungeservice.database.db_util import rollback_errors
from expungeservice.models.expungement_result import EligibilityStatus
from flask_login import current_user


def save_result(request_data, record):
    user_id = current_user.user_id
    search_param_string = user_id + json.dumps(request_data["aliases"], sort_keys=True)
    hashed_search_params = hashlib.sha256(search_param_string.encode()).hexdigest()
    num_charges = len(record.charges)
    num_eligible_charges = len(
        [c for c in record.charges if c.expungement_result.type_eligibility.status == EligibilityStatus.ELIGIBLE]
    )
    _db_insert_result(g.database, user_id, hashed_search_params, num_charges, num_eligible_charges)


@rollback_errors
def _db_insert_result(database, user_id, hashed_search_params, num_charges, num_eligible_charges):
    database.cursor.execute(
        """
        INSERT INTO  SEARCH_RESULTS(search_result_id, user_id, hashed_search_params, num_charges, num_eligible_charges )
        VALUES ( uuid_generate_v4(), %(user_id)s, %(params)s, %(num_charges)s, %(num_eligible_charges)s);
        """,
        {
            "user_id": uuid.UUID(user_id).hex,
            "params": hashed_search_params,
            "num_charges": num_charges,
            "num_eligible_charges": num_eligible_charges,
        },
    )
