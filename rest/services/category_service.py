import csv
import re
import io
from rest.decorators import service
from rest.models import category_model
from rest.constants import NAME, INSTANCE_TYPE, MUTEX_EXCEPTIONS, INSTANCES, GENERALIZATION, \
        PATTERNS, LAST_PROMOTED_INSTANCES, LAST_PROMOTED_PATTERNS, SEED_FILE_EXTENSION

def create(data):
    '''
    Save a category to mongodb, if it donot exist
    @param data: dict with name, instances, patterns, instance_type, generalization,
     mutex_exceptions fields
    @return : category document
    '''
    category = category_model.Category()
    category.name = data[NAME].lower()
    category.generalization = data[GENERALIZATION]
    category.mutex_exceptions = data[MUTEX_EXCEPTIONS]
    category.instances = data[INSTANCES]
    category.instance_type = data[INSTANCE_TYPE]
    category.patterns = data[PATTERNS]
    category.last_promoted_instances = []
    category.last_promoted_patterns = []
    category.save()
    return category

def delete(id):
    '''
    Delete a category from mongodb
    @param id: id of the category to be deleted
    @return category: Deleted document
    '''
    category = category_model.Category.objects.get({'_id': id})
    if category:
        category.delete()
    return category

def update(data):
    '''
    Update a category
    @param data: dict with name, instances, patterns, instance_type, generalization,
     mutex_exceptions fields
    @return count: Number of documents updated
    '''
    category = category_model.Category.objects.get({'_id':data[NAME]})
    category.generalization = data[GENERALIZATION]
    category.mutex_exceptions = data[MUTEX_EXCEPTIONS]
    category.instances = data[INSTANCES]
    category.instance_type = data[INSTANCE_TYPE]
    category.patterns = data[PATTERNS]
    category.last_promoted_instances = data[LAST_PROMOTED_INSTANCES]
    category.last_promoted_patterns = data[LAST_PROMOTED_PATTERNS]
    category.save()
    return category

def get(id):
    '''
    Get the document for the id specified
    @param id: id of the document to be returned
    @return : category object if id is present or else None
    '''
    try:
        category = category_model.Category.objects.get({'_id': id})
        return category
    except:
        return None

def filter(raw_query):
    '''
    Find documents according to the criteria specified
    @return result: document or None
    '''
    return category_model.Category.objects.raw(raw_query)

def list_all():
    '''
    List all categories in mongodb
    @return result: An array of all documents in a collection
    '''
    result = list(category_model.Category.objects.all())
    return result

def list_some(start, limit):
    '''
    List categories according to the limit from mongodb
    @return result: An array of documents
    '''
    qs = category_model.Category.objects.all()
    cursor = qs.aggregate({'$skip': start}, {'$limit': limit})
    result = list(cursor)
    return result

def count():
    '''
    Count number of categories in the collection
    @return count: Categories count
    '''
    count = category_model.Category.objects.count()
    return count

@service(schema=category_model.file_path_schema)
def import_from_filesystem(file_path):
    '''
    Read the seed categories from the file
    @param file_path: path of the file that contains seed categories
    '''
    assert file_path[-4:] == SEED_FILE_EXTENSION
    fp = open(file_path, 'r', encoding='utf-8', errors='ignore')
    reader = csv.DictReader(fp)
    for category in reader:
        category[MUTEX_EXCEPTIONS] = string_to_list(category[MUTEX_EXCEPTIONS])
        category[INSTANCES] = string_to_list(category[INSTANCES])
        category[PATTERNS] = string_to_list(category[PATTERNS])
        category[LAST_PROMOTED_PATTERNS] = []
        category[LAST_PROMOTED_INSTANCES] = []
        create(category)

def import_categories(dataset):
    '''
    Read the seed categories from the file
    @param dataset: Dataset that contains seed categories
    @return count: Number of documents inserted
    '''
    count = 0
    fp = io.StringIO(dataset.file.read().decode('utf-8'))
    reader = csv.DictReader(fp)
    for category in reader:
        if not get(category[NAME]):
            category[MUTEX_EXCEPTIONS] = string_to_list(category[MUTEX_EXCEPTIONS])
            category[INSTANCES] = string_to_list(category[INSTANCES])
            category[PATTERNS] = string_to_list(category[PATTERNS])
            category[LAST_PROMOTED_PATTERNS] = []
            category[LAST_PROMOTED_INSTANCES] = []
            create(category)
            count += 1
    return count

def string_to_list(string):
    '''
    Convert a string of tokens enclosed in double quotes into list of tokens
    @param string: A string of tokens enclosed in double quotes
    @return tokens: A list of tokens
    '''
    regex_pattern = r'"\s+"'
    tokens = []
    string = string.strip()
    if string:
       tokens = re.split(regex_pattern, string[1 : -1])
    return tokens

def list_to_string(tokens):
    '''
    Convert an array of tokens into string of tokens enclosed in double quotes
    @param tokens: A list of tokens
    @return string: A string of tokens with each token enclosed in double quotes
    '''
    string = '" "'.join(tokens).strip()
    if string:
        string = '"' + string + '"'
    return string

@service(schema=category_model.file_path_schema)
def export_csv(file_path):
    '''
    Read the categories from mongodb and write it to a file
    @param file_path: path of the file to which seed categories need to be written
    '''
    assert file_path[-4:] == SEED_FILE_EXTENSION
    csv_file = open(file_path, 'w', encoding='utf-8', errors='ignore')
    writer = csv.writer(csv_file, lineterminator='\n')
    cursor = list_all()
    writer.writerow((NAME, GENERALIZATION, MUTEX_EXCEPTIONS, 
                   INSTANCE_TYPE, INSTANCES, PATTERNS))
    for category in cursor:
        mutex_exceptions = list_to_string(category.mutex_exceptions)
        instances = list_to_string(category.instances)
        patterns = list_to_string(category.patterns)
        writer.writerow((category.name, category.generalization, mutex_exceptions, 
                    category.instance_type, instances, patterns))

def export_categories(categories):
    '''
    Read the categories from mongodb and write it to a file
    @param file_path: path of the file to which seed categories need to be written
    @return csv_file: In memory csv file
    '''
    cursor = filter({'_id' : { '$in': categories}}) if categories else filter({})
    csv_file = io.StringIO()
    writer = csv.writer(csv_file, lineterminator='\n')
    writer.writerow((NAME, GENERALIZATION, MUTEX_EXCEPTIONS, 
                   INSTANCE_TYPE, INSTANCES, PATTERNS))
    for category in cursor:
        mutex_exceptions = list_to_string(category.mutex_exceptions)
        instances = list_to_string(category.instances)
        patterns = list_to_string(category.patterns)
        writer.writerow((category.name, category.generalization, mutex_exceptions, 
                    category.instance_type, instances, patterns))
    csv_file = io.BytesIO(str.encode(csv_file.getvalue()))
    return csv_file


