from flask import jsonify


def handle_error(error):
    """Catch exceptions globally, serialize into JSON, and respond with status code
    Exceptions: BadRequest, NotFound, ServerError
    """
    response = {
    	'detail': error.description,
    	'status': error.code,
    	'title': error.name,
    }
    return jsonify(response), error.code
 
def register_error_handlers(app):
    app.register_error_handler(400, handle_error)
    app.register_error_handler(404, handle_error)
    app.register_error_handler(405, handle_error)
    app.register_error_handler(500, handle_error)