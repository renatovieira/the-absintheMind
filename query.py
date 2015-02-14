def parse_query(query, class_dictionary):
    query_dict = {}
    params = query.split("&")
    for param in params:
        val = param.split("=")
        if val[0] in class_dictionary:
            query_dict[class_dictionary.get(val[0])] = val[1]
    return query_dict