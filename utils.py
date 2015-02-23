from dicttoxml import dicttoxml
import pdb
from flask import Response, jsonify, request


def parse_query(query, class_dictionary):
    return get_dict(query, class_dictionary, None)


def get_dict(query, class_dictionary, query_type):
    query_list = []
    if '&' in query:
        subqueries = query.split('&')
        for subquery in subqueries:
            subquery_list = get_dict(subquery, class_dictionary, '&')
            query_list.extend(subquery_list)
    elif '|' in query:
        subqueries = query.split('|')
        for subquery in subqueries:
            subquery_list = get_dict(subquery, class_dictionary, '|')
            query_list.extend(subquery_list)
    elif query_type == '&':
        if '=' in query:
            params = query.split('=')
            if params[0] in class_dictionary:
                return [[query_type, class_dictionary[params[0]], params[1]]]
            elif params[0].upper() == 'LIMIT' or params[0].upper() == 'OFFSET':
                return [[None, params[0].upper(), params[1]]]
    elif query_type == '|':
        if '=' in query:
            params = query.split('=')
            if params[0] in class_dictionary:
                return [[query_type, class_dictionary[params[0]], params[1]]]
    elif query_type is None:
        params = query.split('=')
        if params[0] in class_dictionary:
            return [['&', class_dictionary[params[0]], params[1]]]
        elif params[0].upper() == 'LIMIT' or params[0].upper() == 'OFFSET':
            return [[None, params[0].upper(), params[1]]]

    return query_list



def xmlify(objects):
    return Response(dicttoxml(objects), mimetype='application/xml')


def get_right_format(objects, request, dao):
    if request.headers['Content-Type'] == 'application/xml':
        objects = [obj.serialize(dao) for obj in objects]
        return xmlify(objects)
    return jsonify(objects=[obj.serialize(dao) for obj in objects])


def json_or_form(request):
    if request.get_json():
        return 'json'
    elif request.form:
        return 'form'
    else:
        return None

