from flask import request, send_file, Response
from rest.decorators import rest_mapping
from rest.services import category_service, dataset_service
from rest.errors import DuplicateIdError, BadRequestError
from rest.constants import NAME, ID, SEED_FILE_EXTENSION
from rest.utils import jsonify


@rest_mapping('/category', ['PUT'])
def save_category():
    """
    Save request body JSON dataset configuration to a Mongo DB
    :return: the saved category JSON
    """
    data = request.get_json(force = True, silent = True)
    if category_service.get(data[NAME]):
        raise DuplicateIdError('Document with same name present in DB')
    return jsonify(category_service.create(data))

@rest_mapping('/category', ['DELETE'])
def delete_category():
    """
    Delete a category from Mongo DB
    :return: the deleted category JSON
    """
    data = request.get_json(force = True, silent = True)
    return jsonify(category_service.delete(data[ID]))

@rest_mapping('/category', ['GET'])
def get_category():
    """
    Find a category from Mongo DB
    :return: the category JSON
    """
    return jsonify(category_service.get(request.args.get('name')))

@rest_mapping('/category/list', ['GET'])
def list_all_categories():
    """
    List categories from Mongo DB
    :return: the categories list JSON
    """
    categories = []
    if request.args.get('start') and request.args.get('limit'):
        start = int(request.args.get('start'))
        limit = int(request.args.get('limit'))
        categories = category_service.list_some(start, limit)
    else:
        categories = category_service.list_all()
    return [jsonify(category) for category in categories]

@rest_mapping('/category/count', ['GET'])
def count_categories():
    """
    Get number of categories in Mongo DB
    :return: count
    """
    return category_service.count()

@rest_mapping('/category/import', ['GET'])
def import_categories():
    """
    Import categories from csv
    :return: list of inserted document ids
    """
    fileid = request.args.get('fileid')
    dataset = dataset_service.get(fileid)
    if dataset.file.filename[-4:] != SEED_FILE_EXTENSION:
        raise BadRequestError('Please select a file with .csv extension')
    count = category_service.import_categories(dataset)
    return count

@rest_mapping('/category/export', ['POST'])
def export_categories():
    """
    Export categories as csv
    :return: csv file
    """
    data = request.get_json(force = True, silent = True)
    file = category_service.export_categories(data['categories'])
    return send_file(filename_or_fp = file, attachment_filename='Categories.csv', as_attachment=True)

@rest_mapping('/authentication-point/authenticate',['POST'])
def alm_authenticate():
    data = request.get_json(force = True, silent = True)
    response = Response()
    response.set_cookie('LWSSO_COOKIE_KEY', 'X8L97zHCONnz79bT_FB_Sc2IQLvW-Gl_vr0dyjvYsbFYvMMhcYgy6-RXWLxMwN7Km3Je4R4hNYD0Sd6FnjHwsq8COqajm3TVwErwgZ4_0AGjLZBBJVXLqqkekmKUbKQLvIhUDsJlciyVkD8wE5Y28_Ow8Mzny9zzB5Jup-bT-4G9dCg__M7EE4dNUWQF-eTZ79_UZ5hOfHqd0JmABqoc9bx7Dk7F67uWvehKSP_cdH-eWKHp9KlPj5Svgim6MMJhLv4j_rDx8sqANXhxBPnvOp_ep1O8wWolGlOa1LFGeXkNZaYUhPKnDi__bhXFBkT8HB0vro_tm1aRP8R7qbW8PcokLkHCcSFzeUnGNHEcuOF1_gRbkGHh-Lgku2Ril-MqhxII-9ypjSizugIb1V88CwDaxQl7IbYRYYxjfzOzXx2y5cEuRk3HAvQ3Mc3uAzM58vJxjKnxziwXfqf0qX7jGXEUKYSa3YGPLewPlb_5Vk2Bb0XRZA45HyGWAIAT465fzEj0khgNxU0T7NvTyDS57gcMTr_SV0cmNtxeVpYHAC4g9RLWqsph3EJVsekIbhv5GOSx5jA_AbNkbDtMkfnN3DASNJpj7gghCAPyYQdH9apm-XQMcXLG4tDb1OGa_N9QW9SKv6z1UMzKzDSbfGSPDSQEf8znpHdArGpMHMFLqPFuncK8l7hEqTNRNSW5Hbb1EJsRsPHm72bWTuqR2zpN5UGGdBTpSITlAK5OqgqNiZ_WjjKQcKjYg2Xu4MES1ulX7_0long6C14BH7E9W5qyxaT-4RgP-d8A5ULsXx14wNbEFmsgBHa0Lmtf_dhj6SGBmAkZOUkMsGPpvwUhp4qH4rjZq2SvXQrdhMkgdnOj_kXCHSzrc2AeR45zboP0sXYcosdK1Af43gNu7mhM1EpgjCFmBFNWPNAPqeSMsk_N6BaCBzexFoJx8I4NiiJ6zTPJd-AUt3LgbTPkLNstjFg_YaWVthIWZRDDSYuHKk-uUFnVfBMfk6JlLqHJvZBbiamnttfIeWAKEoGfEcVfll7ygAKBpiAdZeVkBzt6FQH7f0f9DU9nDNO82PlRYWBgsm0OWpepF75KdXvOsX49lNimxbmW7bcGtMWaAdI7-To8o6vWwTEvuPmUCUP7GjLWkJkvcbzn6e6RmRuwaxuNMOjO6DBGnXBfkYPIjcMQ_xBLrpmkrmC4O8uIvirU3zS9xekQ1CN4LkPAcrCT307CimvPf7kBjz9ANl2d4dhrwgfqbzwumZ-MCvEB5tE9iuSVWxO0l9FqH9naky0rqGJj-fPnF5PSRJAFBy6I8nklNvSHAXY.')
    return response

@rest_mapping('/rest/site-session',['POST'])
def alm_create_site_session():
    data = request.get_json(force = True, silent = True)
    response = Response()
    response.set_cookie('QCSession', 'qcsession_cookie_value')
    response.set_cookie('XSRF-TOKEN', 'xsrf_token_value')
    return response

@rest_mapping('/authentication-point/logout',['GET'])
def alm_logout():
    data = request.get_json(force = True, silent = True)
    response = Response()
    response.set_cookie('LWSSO_COOKIE_KEY', '')
    return response

@rest_mapping('/rest/site-session',['GET'])
def alm_extend_site_session():
    data = request.get_json(force = True, silent = True)
    response = Response()
    response.set_cookie('QCSession', 'qcsession_cookie_value_extended')
    response.set_cookie('XSRF-TOKEN', 'xsrf_token_value_extended')
    return response