from flask import request


def get_request_data():
    """
    Get keys & values from request
    """
    data = request.args.to_dict()

    return data