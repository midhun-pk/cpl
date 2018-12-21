import csv
import re
import io
from rest.decorators import service
from rest.models import relation_model, category_model
from rest.constants import NAME, DOMAIN, RANGE, MUTEX_EXCEPTIONS, INSTANCES, KNOWN_NEGATIVES, \
        PATTERNS, LAST_PROMOTED_INSTANCES, LAST_PROMOTED_PATTERNS, SEED_FILE_EXTENSION

def create(data):
    '''
    Save a relation to mongodb, if doesnot exist
    @param data: dict with name, instances, patterns, domain, range,
     mutex_exceptions, known_negatives fields
    @return : relation document
    '''
    relation = relation_model.Relation()
    relation.name = data[NAME].lower()
    relation.domain = data[DOMAIN]
    relation.range = data[RANGE]
    relation.mutex_exceptions = data[MUTEX_EXCEPTIONS]
    relation.known_negatives = data[KNOWN_NEGATIVES]
    relation.instances = data[INSTANCES]
    relation.patterns = data[PATTERNS]
    relation.last_promoted_instances = []
    relation.last_promoted_patterns = []
    relation.save()
    return relation

def delete(id):
    '''
    Delete a relation from mongodb
    @param id: id of the relation to be deleted
    @return relation: Deleted relation
    '''
    relation = get(id)
    if relation:
        relation.delete()
    return relation

def update(data):
    '''
    Update a relation
    @param data: dict with name, instances, patterns, instance_type, domain, range
     mutex_exceptions fields
    @return count: Number of documents updated
    '''
    relations = list(relation_model.Relation.objects.raw({'_id':data[NAME]}))
    count = len(relations)
    for relation in relations:
        relation.name = data[NAME]
        relation.domain = data[DOMAIN]
        relation.range = data[RANGE]
        relation.mutex_exceptions = data[MUTEX_EXCEPTIONS]
        relation.known_negatives = data[KNOWN_NEGATIVES]
        relation.instances = data[INSTANCES]
        relation.patterns = data[PATTERNS]
        relation.last_promoted_instances = data[LAST_PROMOTED_INSTANCES]
        relation.last_promoted_patterns = data[LAST_PROMOTED_PATTERNS]
        relation.save()
    return count

def get(id):
    '''
    Get the document for the id specified
    @param id: id of the document to be returned
    @return : relation object if id is present or else None
    '''
    try:
        return relation_model.Relation.objects.get({'_id': id})
    except:
        return None

def filter(raw_query):
    '''
    Find documents according to the criteria specified
    @return result: document or None
    '''
    return relation_model.Relation.objects.raw(raw_query)

def list_all():
    '''
    List all relations in mongodb
    @return result: An array of all documents in a collection
    '''
    result = list(relation_model.Relation.objects.all())
    return result

def list_some(start, limit):
    '''
    List realtions according to the limit from mongodb
    @return result: An array of documents
    '''
    qs = relation_model.Relation.objects.all()
    cursor = qs.aggregate({'$skip': start}, {'$limit': limit})
    result = list(cursor)
    return result

@service(schema=relation_model.file_path_schema)
def import_csv(file_path):
    '''
    Read the seed relations from the file
    @param file_path: path of the file that contains seed relations
    '''
    assert file_path[-4:] == SEED_FILE_EXTENSION
    fp = open(file_path, 'r', encoding='utf-8', errors='ignore')
    reader = csv.DictReader(fp)
    for relation in reader:
        relation[DOMAIN] = find_category(relation[DOMAIN])
        relation[RANGE] = find_category(relation[RANGE])
        relation[INSTANCES] = string_to_couples(relation[INSTANCES])
        relation[KNOWN_NEGATIVES] = string_to_couples(relation[KNOWN_NEGATIVES])
        relation[MUTEX_EXCEPTIONS] = string_to_list(relation[MUTEX_EXCEPTIONS])
        relation[PATTERNS] = string_to_list(relation[PATTERNS])
        relation[LAST_PROMOTED_INSTANCES] = []
        relation[LAST_PROMOTED_PATTERNS] = []
        create(relation)

def find_category(name):
    '''
    Find a category from mongodb
    @param name: name of the category to be found
    @return count: category
    '''
    category = category_model.Category.objects.get({'_id':name})
    return category

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

def string_to_couples(string):
    '''
    Convert a string of tokens enclosed in double quotes and paranthesis into list of lists
    @param string: A string of tokens enclosed in double quotes and coupled by paranthesis
    @return couples: A list of lists
    '''
    regex_pattern = r'}\s+{'
    couples = []
    couple_strings = []
    string = string.strip()
    if string:
        couple_strings = re.split(regex_pattern, string[1 : -1])
    if couple_strings:
        for couple_string in couple_strings:
            couples.append(couple_string.strip()[1 : -1].split('","'))     
    return couples

def list_to_string(tokens):
    '''
    Convert an array of tokens into string of tokens enclosed in double quotes
    @param tokens: A list of lists
    @return string: A string of tokens with each token enclosed in double quotes
    '''
    string = '" "'.join(tokens).strip()
    if string:
        string = '"' + string + '"'
    return string

def couples_to_string(couples):
    '''
    Convert an list of lists into string of tokens enclosed in double quotes and coupled by paranthesis
    @param couples: A list of lists
    @return string: A string of tokens with each token enclosed in double quotes
    '''
    couple_strings = []
    for couple in couples:
        couple_string = '","'.join(couple)
        if couple_string:
            couple_strings.append('"' + couple_string.strip() + '"')
    string = '} {'.join(couple_strings)
    if string:
        string = '{' + string + '}'
    return string

@service(schema=relation_model.file_path_schema)
def export_csv(file_path):
    '''
    Read the relations from mongodb and write it to a file
    @param file_path: path of the file to which seed relations need to be written
    '''
    assert file_path[-4:] == SEED_FILE_EXTENSION
    csv_file = open(file_path, 'w', encoding='utf-8', errors='ignore')
    writer = csv.writer(csv_file, lineterminator='\n')
    cursor = list_all()
    writer.writerow((NAME, DOMAIN, RANGE, MUTEX_EXCEPTIONS, 
                    KNOWN_NEGATIVES, INSTANCES, PATTERNS))
    for relation in cursor:
        known_negatives = couples_to_string(relation.known_negatives)
        instances = couples_to_string(relation.instances)
        mutex_exceptions = list_to_string(relation.mutex_exceptions)
        patterns = list_to_string(relation.patterns)
        writer.writerow((relation.name, relation.domain, relation.range, 
                    mutex_exceptions, known_negatives, instances, patterns))

def import_relations(dataset):
    '''
    Read the seed relations from the file
    @param dataset: Dataset that contains seed relations
    @return count: Number of documents inserted
    '''
    count = 0
    fp = io.StringIO(dataset.file.read().decode('utf-8'))
    reader = csv.DictReader(fp)
    for relation in reader:
        if not get(relation[NAME]):
            relation[DOMAIN] = find_category(relation[DOMAIN])
            relation[RANGE] = find_category(relation[RANGE])
            relation[INSTANCES] = string_to_couples(relation[INSTANCES])
            relation[KNOWN_NEGATIVES] = string_to_couples(relation[KNOWN_NEGATIVES])
            relation[MUTEX_EXCEPTIONS] = string_to_list(relation[MUTEX_EXCEPTIONS])
            relation[PATTERNS] = string_to_list(relation[PATTERNS])
            relation[LAST_PROMOTED_INSTANCES] = []
            relation[LAST_PROMOTED_PATTERNS] = []
            create(relation)
            count += 1
    return count

def export_relations(relations):
    '''
    Read the relations from mongodb and write it to a file
    @param file_path: path of the file to which seed relations need to be written
    @return csv_file: In memory csv file
    '''
    cursor = filter({'_id' : { '$in': relations}}) if relations else filter({})
    csv_file = io.StringIO()
    writer = csv.writer(csv_file, lineterminator='\n')
    cursor = list_all()
    writer.writerow((NAME, DOMAIN, RANGE, MUTEX_EXCEPTIONS, 
                    KNOWN_NEGATIVES, INSTANCES, PATTERNS))
    for relation in cursor:
        known_negatives = couples_to_string(relation.known_negatives)
        instances = couples_to_string(relation.instances)
        mutex_exceptions = list_to_string(relation.mutex_exceptions)
        patterns = list_to_string(relation.patterns)
        writer.writerow((relation.name, relation.domain.name, relation.range.name, 
                    mutex_exceptions, known_negatives, instances, patterns))
    csv_file = io.BytesIO(str.encode(csv_file.getvalue()))
    return csv_file

def count():
    '''
    Count number of relations in the collection
    @return count: Relations count
    '''
    count = relation_model.Relation.objects.count()
    return count