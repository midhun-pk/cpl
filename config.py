from pymongo import MongoClient
import os

DATABASE_URI = 'mongodb://localhost:27017/nell'

TAGGER_JAR = 'D:\\Projects\\NLP\\NELL\\tagger\\stanford-postagger-2017-06-09\\stanford-postagger.jar'
TAGGER_MODEL = 'D:\\Projects\\NLP\\NELL\\tagger\\stanford-postagger-2017-06-09\\models\\english-left3words-distsim.tagger'
TAGGER = 'AveragedPerceptron'

# the rest api base prefix
APPLICATION_ROOT = '/cpl'

# the logger level
LOG_LEVEL = 'DEBUG'

# the logger format
LOG_FORMAT = '%(asctime)s %(levelname)s : %(message)s'

# the Flask run mode: PROD or DEBUG
FLASK_RUN_MODE = os.environ.get('MODE') or 'PROD'

# the Flask run port
WEB_PORT = os.environ.get('PORT') or 5000

#Allowed file extensions
ALLOWED_FILE_EXTENSIONS = ['txt', 'csv']

#Static path
STATIC_FOLDER = 'web'