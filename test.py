import re
from rest.models import pattern_learner_model
from rest.constants import NAME
from pymodm.connection import connect
from pymongo import MongoClient
from config import FLASK_RUN_MODE, WEB_PORT, DATABASE_URI, STATIC_FOLDER
from rest.logger import logger
from cpl import learner

def connect_to_db():
    try:
        client = MongoClient(DATABASE_URI)
        client.server_info()
        connect(DATABASE_URI)
        logger.info('Connected to ' + DATABASE_URI)
    except:
        logger.error('Unable to connect to ' + DATABASE_URI)
        exit()

def create(data):
    '''
    Save the couple pattern learner instance in db

    @param data: cpl object to be saved
    @return cpl: saved cpl object
    '''
    from rest.services import dataset_service, category_service, relation_service
    cpl = pattern_learner_model.CPL()
    if not list(pattern_learner_model.CPL.objects.raw({'_id': data[NAME]})):
        cpl.name = data[NAME]
        cpl.iter = 0
        cpl.last_promoted_categories = category_service.list_all()
        cpl.last_promoted_relations = relation_service.list_all()
    '''
    corpus = dataset_service.read(data[DATASET], 'uploads').decode('utf-8')
    corpus = re.split(r'[\n\t]+', corpus)
    #prepocessor.preprocess_corpus(corpus)
    '''
    f = open('docs/StudentRegistration.txt', 'r', encoding='utf-8', errors='ignore')
    corpus = f.read()
    corpus = re.split(r'[\n\t]+', corpus)
    while cpl.last_promoted_categories or cpl.last_promoted_relations:
        categories, relations = learner.learn(corpus, cpl)
        cpl.iter += 1
        print(cpl.iter)
        #cpl.save()
    #cpl.last_promoted_categories = categories.values()
    #cpl.last_promoted_relations = relations.values()'''

data = {
  'name' : 'LEARNER - 1',
  'dataset' : '5ab28a275d76c92acce21095'
}
connect_to_db()
create(data)
