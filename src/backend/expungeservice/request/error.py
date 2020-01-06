from flask import abort, jsonify, make_response
import logging

def error(code, message):
    logging.error("code %i %s" % (code, message), stack_info = True)
    abort(make_response(jsonify(message=message), code))
