from rest.services import pattern_learner_service
def learn(data):
    pattern_learner_service.create(data)
    #category_service.update_categories(categories)