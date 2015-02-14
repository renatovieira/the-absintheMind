from country import Country
from city import City


def parse_country_query(query):
    query_dict = {}
    params = query.split("&")
    dictionary = Country.field_to_database_column()
    for param in params:
        val = param.split("=")
        if val[0] in dictionary:
            query_dict[dictionary.get(val[0])] = val[1]
    return query_dict


def parse_city_query(query):
    query_dict = {}
    params = query.split("&")
    dictionary = City.field_to_database_column()
    for param in params:
        val = param.split("=")
        if val[0] in dictionary:
            query_dict[dictionary.get(val[0])] = val[1]
    return query_dict