import gridfs
import io
from rest.decorators import service
from rest.models import dataset_model
from bson.objectid import ObjectId
from pymodm.files import File
from rest.constants import NAME, DESCRIPTION

def download_to_filesystem(id, collection, download_path):
    '''
    Download dataset from mongodb to a folder

    @param id: _id of the document
    @param collection: Name of collection from which the document needs to be downloaded
    @param download_path: The folder to which document should be downloaded
    @return download_path: path to the downloaded file
    '''
    fp = open(download_path,'wb+')
    dataset = dataset_model.Dataset.objects.get({'_id':ObjectId(id)})
    data = dataset.file.read()
    fp.write(data)
    return download_path

def download(id):
    '''
    Download dataset from mongodb

    @param id: the document dict
    @return file: downloaded file
    '''
    dataset = dataset_model.Dataset.objects.get({'_id':ObjectId(id)})
    file = io.BytesIO(dataset.file.read())
    return file

def upload(file, filename, data):
    '''
    Upload a dataset to mongodb.
    Upload only if no file with same name already exists in the mongodb

    @param file: file to be uploaded
    @param filename: Actual name of file in file system
    @param data: details about file
    @return dataset: Uploaded dataset
    '''
    dataset = dataset_model.Dataset()
    dataset.name = data[NAME]
    dataset.description = data[DESCRIPTION]
    dataset.file = File(file, name=filename)
    dataset.save()
    return dataset

def delete(data):
    '''
    Delete a dataset from mongodb
    @param data: the document dict
    @return dataset: Deleted dataset
    '''
    if get(data['_id']):
        dataset = dataset_model.Dataset.from_document(data)
        dataset.file.delete()
        dataset.delete()
        return dataset

def filter(raw_query):
    '''
    Find documents according to the criteria specified
    @return result: document or None
    '''
    return dataset_model.Dataset.objects.raw(raw_query)

def read(data):
    '''
    Read dataset from mongodb

    @param data: the document dict
    @return data: data read from the mongo file
    '''
    dataset = dataset_model.Dataset.from_document(data)
    data = dataset.file.read()
    return data

def get(id):
    '''
    Get the document for the id specified
    @param id: id of the document to be returned
    @return : dataset object if id is present or else None
    '''
    try:
        return dataset_model.Dataset.objects.get({'_id': id})
    except:
        return None

def find(name):
    '''
    Get the document for the name specified
    @param name: name of the document to be returned
    @return : dataset object if name is present or else None
    '''
    try:
        return filter({'name': name})
    except:
        return None

def list_all():
    '''
    List all datasets in mongodb
    @return result: An array of all documents in a collection
    '''
    result = list(dataset_model.Dataset.objects.all())
    result.reverse()
    return result

def list_some(start, limit):
    '''
    List datasets according to the limit from mongodb
    @return result: An array of documents
    '''
    qs = dataset_model.Dataset.objects.all()
    cursor = qs.aggregate({'$skip': start}, {'$limit': limit})
    result = list(cursor)
    return result

def count():
    '''
    Count number of datasets in the collection
    @return count: Datasets count
    '''
    count = dataset_model.Dataset.objects.count()
    return count