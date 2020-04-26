from flask import abort, current_app, jsonify, make_response


def error(code, message):
    current_app.logger.error("code %i %s" % (code, message), stack_info=True)
    return abort(make_response(jsonify(message=message), code))


def check_data_fields(request_json, required_fields):
    if not all([field in request_json.keys() for field in required_fields]):
        error(400, "missing one or more required fields: " + str(required_fields))
