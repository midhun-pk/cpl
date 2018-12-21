from flask import request, send_file
from rest.decorators import rest_mapping
from rest.services import dataset_service, dataset_service
from rest.errors import DuplicateIdError, BadRequestError
from rest.constants import NAME, ID
from rest.utils import jsonify, dejsonify, is_allowed
from werkzeug.utils import secure_filename
import json

@rest_mapping('/dataset', ['POST'])
def upload_dataset():
    """
    Save request body JSON dataset configuration to a Mongo DB
    @return: the saved dataset JSON
    """
    print(request.form)
    if 'file' not in request.files:
        raise BadRequestError('No file selected')
    file = request.files['file']
    if file.filename == '':
        raise BadRequestError('No file selected')
    if not is_allowed(file.filename):
        raise BadRequestError('File not allowed')
    if file:
        filename = secure_filename(file.filename)
        return jsonify(dataset_service.upload(file, filename, request.form))
        

@rest_mapping('/dataset/download', ['GET'])
def download_dataset():
    """
    Download dataset from Mongo DB
    @return: dataset File
    """
    id = request.args.get('_id')
    file = dataset_service.download(id)
    return send_file(filename_or_fp = file, attachment_filename='Relations.csv', as_attachment=True)

@rest_mapping('/dataset', ['DELETE'])
def delete_dataset():
    """
    Delete a dataset from Mongo DB
    @return: the deleted dataset JSON
    """
    data = request.get_json()
    return jsonify(dataset_service.delete(data))

@rest_mapping('/dataset/name', ['GET'])
def get_datasets():
    """
    Find a dataset from Mongo DB
    @return: the dataset JSON
    """
    name = request.args.get('name')
    return [jsonify(dataset) for dataset in list(dataset_service.find(name))]

@rest_mapping('/dataset', ['GET'])
def list_all_datasets():
    """
    List datasets from Mongo DB
    @return: the datasets list JSON
    """
    datasets = []
    if request.args.get('start') and request.args.get('limit'):
        start = int(request.args.get('start'))
        limit = int(request.args.get('limit'))
        datasets = dataset_service.list_some(start, limit)
    else:
        datasets = dataset_service.list_all()
    return [jsonify(dataset) for dataset in datasets]

@rest_mapping('/dataset/count', ['GET'])
def count_datasets():
    """
    Get number of datasets in Mongo DB
    @return: count
    """
    return dataset_service.count()