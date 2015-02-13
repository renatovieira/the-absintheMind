from country import Country


def parse_country_query(query):
    query_dict = {}
    params = query.split("&")
    country_dict = Country.field_to_database_column()
    for param in params:
        val = param.split("=")
        if val[0] in country_dict:
            query_dict[country_dict.get(val[0])] = val[1]
    return query_dict