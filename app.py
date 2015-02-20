#!flask/bin/python
from flask import Flask, request, abort, jsonify
from pymysql import IntegrityError
import pymysql
import pdb
from dao import Dao
from country import Country
from city import City
from address import Address
from customer import Customer
from utils import *

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

dao = Dao()

#Country

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = dao.get_countries()
    return get_right_format(countries, request)

@app.route('/countries', methods=['POST'])
def create_country():
    #return request
    return dao.create_row_in_country(request)

@app.route('/countries/<int:country_id>', methods=['DELETE'])
def del_country_by_id(country_id):
    temp = dao.delete_country_by_id(country_id)
    if not temp:
        abort(404)
    else:
        return dao.delete_country_by_id(country_id)

@app.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    country = dao.find_country_by_id(country_id)
    if not request.json:
        abort(400)
    #get all parameters send via curl
    dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    country.name = dictionary.get('name', country.name)
    #update on the db
    dao.update_country(country)
    #return updated object
    return jsonify({'country': country.serialize()})

@app.route('/countries/q/<query>', methods=['GET'])
def query_countries(query):
    query_dict, and_query = parse_query(query, Country.field_to_database_column())
    countries = dao.query_countries(query_dict, and_query)
    return get_right_format(countries, request)

#City

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = dao.get_cities()
    return get_right_format(cities, request)

@app.route('/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    cities = dao.find_cities_by_country_id(country_id)
    return get_right_format(cities, request)

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    temp = dao.delete_city_by_id(city_id)
    if not temp:
        abort(404)
    else:
        return dao.delete_city_by_id(city_id)

@app.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    city = dao.find_city_by_id(city_id)
    if not request.json:
        abort(400)
    #get all parameters send via curl
    dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    city.name = dictionary.get('name', city.name)
    city.country_id = dictionary.get('country_id', city.country_id)
    #update on the db
    dao.update_city(city)
    #return updated object
    return jsonify({'city': city.serialize()})

@app.route('/cities/q/<query>', methods=['GET'])
def query_cities(query):
    query_dict, and_query = parse_query(query, City.field_to_database_column())
    cities = dao.query_cities(query_dict, and_query)
    return get_right_format(cities, request)

@app.route('/cities', methods=['POST'])
def create_city():
    return dao.create_row_in_city(request)

#Address

@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = dao.get_addresses()
    return get_right_format(addresses, request)

@app.route('/addresses/country/<int:country_id>', methods=['GET'])
def get_addresses_by_country(country_id):
    addresses = dao.find_addresses_by_country(country_id)
    return get_right_format(addresses, request)

@app.route('/addresses/city/<int:city_id>', methods=['GET'])
def get_addresses_by_city(city_id):
    addresses = dao.find_addresses_by_city(city_id)
    return get_right_format(addresses, request)

@app.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    address = dao.find_address_by_id(address_id)
    if not request.json:
        abort(400)
    #get all parameters sent via curl
    dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    address.address1 = dictionary.get('address1', address.address1)
    address.address2 = dictionary.get('address2', address.address2)
    address.district = dictionary.get('district', address.district)
    address.postal_code = dictionary.get('postal_code', address.postal_code)
    address.city_id = dictionary.get('city_id', address.city_id)
    address.country_id = dictionary.get('country_id', address.country_id)
    #update on the db
    dao.update_address(address)
    #return updated object
    return jsonify({'address': address.serialize()})


@app.route('/addresses', methods=['POST'])
def create_address():
    return dao.create_row_in_address(request)

@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address_by_id(address_id):
    temp = dao.delete_address_by_id(address_id)
    if not temp:
        abort(404)
    else:
        return dao.delete_address_by_id(address_id)

@app.route('/addresses/q/<query>', methods=['GET'])
def query_addresses(query):
    query_dict, and_query = parse_query(query, Address.field_to_database_column())
    addresses = dao.query_addresses(query_dict, and_query)
    return get_right_format(addresses, request)

#Customer

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = dao.get_customers()
    return get_right_format(customers, request)

@app.route('/customers/country/<int:country_id>', methods=['GET'])
def get_customers_by_country(country_id):
    customers = dao.find_customers_by_country(country_id)
    return get_right_format(customers, request)

@app.route('/customers/city/<int:city_id>', methods=['GET'])
def get_customers_by_city(city_id):
    customers = dao.find_customers_by_city(city_id)
    return get_right_format(customers, request)

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = dao.find_customer_by_id(customer_id)
    if not request.json:
        abort(400)
    #get all parameters sent via curl
    dictionary = request.json
    #update all parameters that were sent, keep information same if a parameter has not been sent
    customer.name.first = dictionary.get('first_name', customer.name.first)
    customer.name.last = dictionary.get('last_name', customer.name.last)
    customer.email_id = dictionary.get('email_id', customer.email_id)
    customer.store_id = dictionary.get('store_id', customer.store_id)
    customer.address_id = dictionary.get('address_id', customer.address_id)
    customer.active = dictionary.get('active', customer.active)
    customer.create_date = dictionary.get('create_date', customer.create_date)
    #update on db
    dao.update_customer(customer)
    #return updated object
    return jsonify({'customer': customer.serialize()})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    temp = dao.delete_customer_by_id(customer_id)
    if not temp:
        abort(404)
    else:
        return dao.delete_customer_by_id(customer_id)

@app.route('/customers', methods=['POST'])
def create_customer():
    return dao.create_row_in_customer(request)

@app.route('/customers/q/<query>', methods=['GET'])
def query_customer(query):
    query_dict, and_query = parse_query(query, Customer.field_to_database_column())
    customers = dao.query_customers(query_dict, and_query)
    return get_right_format(customers, request)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
