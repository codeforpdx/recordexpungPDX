from flask import abort, jsonify, make_response
import logging


def error(code, message):
    logging.error("code %i %s" % (code, message), stack_info=True)
    abort(make_response(jsonify(message=message), code))


def check_data_fields(request_json, required_fields):
    if not all([field in request_json.keys() for field in required_fields]):
        error(400, "missing one or more required fields: " + str(required_fields))
