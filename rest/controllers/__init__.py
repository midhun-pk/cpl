"""
Initializer of routes for Flask application.
The controller functions will auto import into Flask app if function has a rest_mapping decorator
"""
from rest.decorators import inject_flask_app


def init(flask_app):
    """
    Import all controller functions, so that all routes can register into the Flask app
    :param flask_app: the Flask app instance
    :return: None
    """
    inject_flask_app(flask_app)
    from rest.controllers import category_controller
    from rest.controllers import relation_controller
    from rest.controllers import dataset_controller
