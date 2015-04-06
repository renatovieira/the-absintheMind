from dicttoxml import dicttoxml
import pdb
from flask import Response, jsonify, request
from page_obj import Page

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


def get_right_format(objects, request, dao, page=None):
    #pdb.set_trace()
    if request.headers.get('Content-Type', '') == 'application/xml':
        objects = [obj.serialize(dao) for obj in objects]
        if page:
            return xmlify(objects+page)
        else:
            return xmlify(objects)
    if page:
        page = [page.serialize()]
        return jsonify({'objects':[obj.serialize(dao) for obj in objects]+page})
    else:
        return jsonify(objects=[obj.serialize(dao) for obj in objects])


def json_or_form(request):
    if request.get_json():
        return 'json'
    elif request.form:
        return 'form'
    else:
        return None

def paginate(items, per_page, page_url):
    i = 0
    page_num = 1
    pages = []
    while i < len(items):
        temp_page = Page(items[i:i+per_page])
        # if we're not on the first page there has to be a previous page link
        if page_num > 1:
            temp_page.prev_page = "http://127.0.0.1:5000/{0}/{1}".format(page_url,page_num-1)

        # increase the page number
        page_num += 1
        i = i+per_page
        # don't add a next page if we are at the end of the list
        try:
            items[i]
            temp_page.next_page = "http://127.0.0.1:5000/{0}/{1}".format(page_url,page_num)
            pages.append(temp_page)
        except IndexError:
            pages.append(temp_page)
            continue

    return pages
