from config import ALLOWED_FILE_EXTENSIONS
from bson import json_util
import json

def jsonify(mongo_object):
    '''
    Convert the Mongo object to dictionary
    @param mongo_object: Mongo pymodm object
    @return :dictionay object
    '''
    if not mongo_object:
        return None
    else: 
        try:
            return json.loads(json_util.dumps(mongo_object.__dict__['_data']))
        except:
            return json.loads(json_util.dumps(mongo_object))

def dejsonify(json):
    '''
    Convert the dictionary to Mongo object
    @param json: json object
    @return :dictionay object
    '''
    return None if not json else json_util.loads(json)

def is_allowed(filename):
    '''
    Check whether the file is allowed or not
    @param filename: Name of the file
    @return : Boolean value
    '''
    return filename.split('.')[-1] in ALLOWED_FILE_EXTENSIONS