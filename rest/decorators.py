import inspect
import re
from functools import wraps
from bson.objectid import ObjectId
from flask import jsonify, Response
from rest.errors import BadRequestError
from config import APPLICATION_ROOT
from .logger import logger
from cerberus import Validator
from flask_cors import CORS, cross_origin

# the cached flask app
app = None

# the cerberus validator instance
cerberus_validator = Validator()

def inject_flask_app(flask_app):
    """
    Inject Flask app and cache it for auto registering routes
    :param flask_app: the Flask app instance
    :return: None
    """
    global app
    app = flask_app
    CORS(app)

def rest_mapping(path, methods=None):
    """
    The REST mapping decorator, used for registering path to the Flask app and wrapping result into JSON response
    :param path: the route path
    :param methods: the request methods
    :return: the decorator
    """

    def decorator(func):
        @wraps(func)
        @cross_origin()
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) == Response: return result
            return result is None and '' or jsonify(result)  # wrap json response

        new_path = APPLICATION_ROOT + path  # add path prefix to path
        logger.debug('endpoint added: ' + (methods and methods.__str__() or '[ALL]') + ' ' + new_path)
        app.route(new_path, methods=methods)(wrapper)  # inject route to Flask app
        
        return wrapper

    return decorator

class CustomValidator(Validator):
    def _validate_type_objectid(self, value):
        '''
        Enables validation for `objectid` schema attribute.

        @param value: field value.
        '''
        result = True
        if type(value) != ObjectId:
            result = False
        if not re.match('[a-f0-9]{24}', value):
            result = False
        return result

def service(schema = None):
    '''
    The REST service decorator, used for parameter check and logging service method entrance/exit with
    parameters and result

    @param schema: the validator schema
    @return: the decorator
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if schema is not None:
                document = {}
                args_len = len(args)
                args_spec = inspect.getfullargspec(func)
                for i, document_key in enumerate(args_spec.args):
                    if i >= args_len:
                        document[document_key] = kwargs.get(document_key) or args_spec.defaults[i - args_len]
                    else:
                        document[document_key] = args[i]

                if not cerberus_validator.validate(document, schema):
                    print(cerberus_validator.errors)
            
            service_result = func(*args, **kwargs)
            return service_result
        return wrapper
    return decorator

