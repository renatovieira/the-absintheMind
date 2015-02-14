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
    print query_dict
    return query_dict