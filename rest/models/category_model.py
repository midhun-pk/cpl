from pymodm import MongoModel, fields
from pymodm.queryset import QuerySet
from pymodm.manager import Manager


class Category(MongoModel):
    name = fields.CharField(primary_key = True, required = True)
    generalization = fields.CharField()
    mutex_exceptions = fields.ListField(fields.CharField(), blank = True)
    instances = fields.ListField(fields.CharField(), blank = True)
    instance_type = fields.CharField(blank = True)
    patterns = fields.ListField(fields.CharField(), blank = True)
    last_promoted_patterns = fields.ListField(fields.CharField(), blank = True)
    last_promoted_instances = fields.ListField(fields.CharField(), blank = True)
    objects = Manager()


file_path_schema = {
    'file_path': {
        'type': 'string',
        'required': True,
        'nullable': False,
        'empty': False
    }
}
