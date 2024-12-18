import os
from flask import jsonify

def scan_recurse(base_dir):
    try:
        for entry in os.scandir(base_dir):
            if entry.is_file():
                yield entry
            else:
                yield from scan_recurse(entry.path)
    except Exception as e:
        return str(e)

def make_response(success, message, data=None, status_code=200):
    response = {
        "success": success,
        "message": message
    }
    if data:
        response["data"] = data
    return jsonify(response), status_code

def handle_error(message, status_code=400):
    return make_response(False, message, status_code=status_code)