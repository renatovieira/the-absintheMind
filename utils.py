from dicttoxml import dicttoxml
import pdb
from flask import Response, jsonify, request
from page_obj import Page

def parse_query(query, class_dictionary):
    if '&' in query:
        return get_dict(query, class_dictionary, '&'), True
    return get_dict(query, class_dictionary, '|'), False


def get_dict(query, class_dictionary, delimiter):
    query_dict = []
    params = query.split(delimiter)
    for param in params:
        val = param.split("=")
        if val[0] in class_dictionary:
            query_dict.append([class_dictionary.get(val[0]), val[1]])
        elif val[0].upper() == 'OFFSET' or val[0].upper() == 'LIMIT':
            query_dict.append([val[0].upper(), val[1]])
    return query_dict


def xmlify(objects):
    return Response(dicttoxml(objects), mimetype='application/xml')


def get_right_format(objects, request):
    if request.headers['Content-Type'] == 'application/xml':
        objects = [obj.serialize() for obj in objects]
        return xmlify(objects)
    return jsonify(objects=[obj.serialize() for obj in objects])


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
