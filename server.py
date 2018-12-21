import os
import glob
from http import HTTPStatus
from pymodm.connection import connect
from pymongo import MongoClient
from flask import Flask, render_template
from rest.errors import error_handler
from test import runner
from rest.logger import logger
from rest.controllers import init
from config import FLASK_RUN_MODE, WEB_PORT, DATABASE_URI, STATIC_FOLDER
from web_config import config


# create new Flask app
app = Flask(__name__, template_folder=STATIC_FOLDER, static_folder=STATIC_FOLDER)


@app.route('/<path>')
def start(path):
    return render_template('modules/core/views/index.view.html', files=files)


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
@app.errorhandler(HTTPStatus.NOT_FOUND)
@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
@app.errorhandler(Exception)
def app_error_handler(err):
    """
    Handle all errors
    :param err: the error instance
    :return: the JSON response with error message
    """
    return error_handler(err)

def connect_to_db():
    try:
        client = MongoClient(DATABASE_URI)
        client.server_info()
        connect(DATABASE_URI)
        logger.info('Connected to ' + DATABASE_URI)
    except:
        logger.error('Unable to connect to ' + DATABASE_URI)
        exit()

def glob_path(relative_paths):
    """
    Get the globbed path of file
    @param relative_paths: Relative paths of the files
    @return globbed paths: Globbed paths of the files
    """
    globbed_paths = []
    for relative_path in relative_paths:
        relative_path = os.path.join(STATIC_FOLDER, relative_path)
        paths = [path.replace('\\', '/')[len(STATIC_FOLDER) + 1:] for path in glob.glob(relative_path)]
        globbed_paths.extend(paths)
    return globbed_paths

def initialize_files(config):
    """
    Initialize all files in the config
    @param config: dictionary with absolute path
    @return modified_config: config with absolute path
    """
    modified_config = {}
    modified_config['title'] = config['title']
    modified_config['css'] = []
    modified_config['js'] = []
    modified_config['css'] = config['lib']['css']
    modified_config['js'] = config['lib']['js']
    modified_config['css'].extend(glob_path(config['css']))
    modified_config['js'].extend(glob_path(config['js']))
    return modified_config



if __name__ == '__main__':

    '''
    id = dataset_service.upload('ame', 'uploads', './docs/data.txt')
    print(id)
    if id:
        path = dataset_service.download(id, 'uploads', './docs/data2.txt')
        print(path)
    '''
    files = initialize_files(config)
    logger.info('Connecting to Mongo database...')
    db_response = connect_to_db()
    #from rest.services import dataset_service
    #dataset_service.upload('Seed relation 1', 'dataset', './docs/Relations.csv')
    logger.info('Starting app at port = {0}, with mode = {1}'.format(WEB_PORT, FLASK_RUN_MODE))
    init(app)
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD']=True
    #app.run(debug=(FLASK_RUN_MODE == 'DEBUG'), port=int(WEB_PORT))
    #print(client.server_info())
    #category_service.import_csv('./docs/Categories.csv')
    #print(category_service.delete('page'))
    #category_service.export_csv('./docs/Categories_new.csv')
    '''
    result = category_service.list_all()
    for doc in result:
        deleted_count = category_service.delete(str(doc['_id']))
        print(deleted_count)
    '''
    
    #relation_service.import_csv('./docs/Relations.csv')
    #relation_service.export_csv('./docs/Relations_new.csv')
    '''
    result = relation_service.list_all()
    for doc in result:
        deleted_count = relation_service.delete(str(doc['_id']))
        print(deleted_count)
    
    '''
    #runner.run()
    #dataset_service.upload('second corpus', 'uploads', './docs/StudentRegistration.txt')
    #dataset_service.delete('5ab288785d76c91b50cccf92', 'uploads')
    #dataset_service.read('5ab28a275d76c92acce21095', 'uploads')
    #dataset_service.download('5ab28a275d76c92acce21095', 'uploads', './docs/SRS_sample_web_app2.txt')
    '''
    data = {
        'name' : 'LEARNER - 1',
        'dataset' : '5ab28a275d76c92acce21095'
    }'''
    data = {
        'name' : 'LEARNER - 2',
        'dataset' : '5ab4e4295d76c925c4b90275'
    }
    from rest.controllers import pattern_learner_controller
    pattern_learner_controller.learn(data)
    #extract()
    





