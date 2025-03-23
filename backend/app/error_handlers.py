from flask import jsonify
from werkzeug.exceptions import HTTPException
from app.api.errors import error_response

def register_error_handlers(app):
    @app.errorhandler(400)
    def handle_bad_request(error):
        return error_response(400, str(error))
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return error_response(404, str(error))
    
    @app.errorhandler(500)
    def handle_server_error(error):
        return error_response(500, str(error))
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return error_response(error.code, error.description)
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {error}", exc_info=True)
        return error_response(500, "An unexpected error occurred")