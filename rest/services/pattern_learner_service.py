import re
from cpl import learner, prepocessor
from rest.services import dataset_service, category_service, relation_service
from rest.decorators import service
from rest.models import pattern_learner_model
from rest.constants import NAME, ITER, LAST_PROMOTED_CATEGORIES, LAST_PROMOTED_RELATIONS, DATASET

def create(data):
    '''
    Save the couple pattern learner instance in db

    @param data: cpl object to be saved
    @return cpl: saved cpl object
    '''
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
    while cpl.last_promoted_categories or cpl.last_promoted_relations:
        categories, relations = learner.learn(corpus, cpl)
        cpl.iter += 1
        print(cpl.iter)
        #cpl.save()
    #cpl.last_promoted_categories = categories.values()
    #cpl.last_promoted_relations = relations.values()'''
    