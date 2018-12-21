from pymodm import MongoModel, fields
from pymodm.queryset import QuerySet
from pymodm.manager import Manager
from pymodm.files import FieldFile

class DatasetFile(MongoModel):
    filename = fields.CharField()

class Dataset(MongoModel):
    name = fields.CharField(required = True)
    description = fields.CharField()
    file = fields.FileField()
    objects = Manager()


upload_schema = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'collection': {
        'type': 'string',
        'allowed': ['uploads', 'results'],
        'required': True
    },
    'file_path': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}

download_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'collection': {
        'type': 'string',
        'allowed': ['uploads', 'results'],
        'required': True
    },
    'download_path': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}

delete_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'collection': {
        'type': 'string',
        'allowed': ['uploads', 'results'],
        'required': True
    }
}

read_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'collection': {
        'type': 'string',
        'allowed': ['uploads', 'results'],
        'required': True
    }
}
