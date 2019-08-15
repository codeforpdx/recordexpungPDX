from flask import abort
import logging

def error(code, message):
    logging.error("code %i %s" % (code, message), stack_info = True)
    abort(code, message)