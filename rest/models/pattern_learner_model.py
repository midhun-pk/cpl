from pymodm import MongoModel, fields
from pymodm.queryset import QuerySet
from pymodm.manager import Manager
from rest.models.category_model import Category
from rest.models.relation_model import Relation


class CPL(MongoModel):
    name = fields.CharField(primary_key = True, required = True)
    iter = fields.IntegerField(required = True)
    last_promoted_categories = fields.ListField(fields.ReferenceField(Category), blank = True)
    last_promoted_relations = fields.ListField(fields.ReferenceField(Relation), blank = True)
    objects = Manager()

id_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}

