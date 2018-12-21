from flask import request, send_file
from rest.decorators import rest_mapping
from rest.services import relation_service, dataset_service
from rest.errors import DuplicateIdError, BadRequestError
from rest.constants import NAME, ID, SEED_FILE_EXTENSION
from rest.utils import jsonify

@rest_mapping('/relation', ['PUT'])
def save_relation():
    """
    Save request body JSON dataset configuration to a Mongo DB
    :return: the saved relation JSON
    """
    data = request.get_json(force = True, silent = True)
    if relation_service.get(data[NAME]):
        raise DuplicateIdError('Document with same name present in DB')
    return jsonify(relation_service.create(data))

@rest_mapping('/relation', ['DELETE'])
def delete_relation():
    """
    Delete a relation from Mongo DB
    :return: the deleted relation JSON
    """
    data = request.get_json(force = True, silent = True)
    return jsonify(relation_service.delete(data[ID]))

@rest_mapping('/relation', ['GET'])
def get_relation():
    """
    Find a relation from Mongo DB
    :return: the relation JSON
    """
    return jsonify(relation_service.get(request.args.get('name')))

@rest_mapping('/relation/list', ['GET'])
def list_all_relations():
    """
    List relations from Mongo DB
    :return: the relations list JSON
    """
    relations = []
    if request.args.get('start') and request.args.get('limit'):
        start = int(request.args.get('start'))
        limit = int(request.args.get('limit'))
        relations = relation_service.list_some(start, limit)
    else:
        relations = relation_service.list_all()
    return [jsonify(relation) for relation in relations]

@rest_mapping('/relation/count', ['GET'])
def count_relations():
    """
    Get number of relations in Mongo DB
    :return: count
    """
    return relation_service.count()

@rest_mapping('/relation/import', ['GET'])
def import_relations():
    """
    Import relations from csv
    :return: list of inserted document ids
    """
    fileid = request.args.get('fileid')
    dataset = dataset_service.get(fileid)
    if dataset.file.filename[-4:] != SEED_FILE_EXTENSION:
        raise BadRequestError('Please select a file with .csv extension')
    count = relation_service.import_relations(dataset)
    return count

@rest_mapping('/relation/export', ['POST'])
def export_relations():
    """
    Export relations as csv
    :return: csv file
    """
    data = request.get_json(force = True, silent = True)
    file = relation_service.export_relations(data['relations'])
    return send_file(filename_or_fp = file, attachment_filename='Relations.csv', as_attachment=True)