#!flask/bin/python
from flask import Flask, jsonify, request
from dao import Dao
from query import *

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app


dao = Dao()

#Country

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = dao.get_countries()
    return jsonify(countries=[country.serialize() for country in countries])

@app.route('/countries/<int:country_id>', methods=['DELETE'])
def del_country_by_id(country_id):
    return dao.delete_country_by_id(country_id)

@app.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    country = dao.find_country_by_id(country_id)
    if not request.json:
        abort(400)
    #get all parameters send via curl
    dict = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    country.name = dict.get('name', country.name)
    #update on the db
    dao.update_country(country)
    #return updated object
    return jsonify({'country': country.serialize()})

@app.route('/countries/q="<query>"', methods=['GET'])
def query_countries(query):
    query_dict = parse_country_query(query)
    countries = dao.query_countries(query_dict)
    return jsonify(countries=[country.serialize() for country in countries])

#City

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = dao.get_cities()
    return jsonify(cities=[city.serialize() for city in cities])

@app.route('/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    return jsonify(cities=[city.serialize() for city in dao.find_cities_by_country_id(country_id)])

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    return dao.delete_city_by_id(city_id)

@app.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    city = dao.find_city_by_id(city_id)
    if not request.json:
        abort(400)
    #get all parameters send via curl
    dict = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    city.name = dict.get('name', city.name)
    city.country_id = dict.get('country_id', city.country_id)
    #update on the db
    dao.update_city(city)
    #return updated object
    return jsonify({'city': city.serialize()})

#Address

@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = dao.get_addresses()
    return jsonify(addresses=[address.serialize() for address in addresses])

@app.route('/addresses/country/<int:country_id>', methods=['GET'])
def get_addresses_by_country(country_id):
    return jsonify(addresses=[address.serialize() for address in dao.find_addresses_by_country(country_id)])

@app.route('/addresses/city/<int:city_id>', methods=['GET'])
def get_addresses_by_city(city_id):
    return jsonify(addresses=[address.serialize() for address in dao.find_addresses_by_city(city_id)])

@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address_by_id(address_id):
    return dao.delete_address_by_id(address_id)

#Customer

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = dao.get_customers()
    return jsonify(customers=[customer.serialize() for customer in customers])

@app.route('/customers/country/<int:country_id>', methods=['GET'])
def get_customers_by_country(country_id):
    return jsonify(customers=[customer.serialize() for customer in dao.find_customers_by_country(country_id)])

@app.route('/customers/city/<int:city_id>', methods=['GET'])
def get_customers_by_city(city_id):
    return jsonify(customers=[customer.serialize() for customer in dao.find_customers_by_city(city_id)])

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    return dao.delete_customer_by_id(customer_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
