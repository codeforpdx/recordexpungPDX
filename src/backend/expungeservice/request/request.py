from expungeservice.request.error import error

def check_data_fields(request_json, required_fields):
    if not all([field in request_json.keys() for field in required_fields]):
        error(400, "missing one or more required fields: " + str(required_fields))
