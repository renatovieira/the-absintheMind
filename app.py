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
@app.route('/combined', methods=['POST'])
def test_combine():
    #process the request data
    jf = json_or_form(request)
    country = {}
    if jf is 'json':
        c_name = request.json['CountryName']
        city = {
            'CityID': request.json['CityID'],
            'CityName': "'{0}'".format(request.json['CityName'])
        }
    elif jf is 'form':
        c_name = request.form['CountryName']
        city = {
            'CityID': request.form['CityID'],
            'CityName': request.form['CityName']
        }
    else:
        abort(400)

    # find out the country id
    temp_country = dao.find_country_by_name(c_name)
    if not temp_country:
        #temp solution, until we change the db schema
        new_country_data = {
            'CountryID': 100,
            'CountryName': "'{0}'".format(c_name)
        }

        new_country = Country(new_country_data)
        new_uri = dao.create_row_in_country(new_country)
        #temp solution because of what create_row returns right now (uri string)
        city['CountryID'] = int(new_uri[(new_uri.rfind('/')+1):])
    else:
        city['CountryID'] = temp_country.id

    #need new create row in city method but call it here
    return 'hi'

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = dao.get_countries()
    return get_right_format(countries, request)

@app.route('/countries', methods=['POST'])
def create_country():
    #return request
    jf = json_or_form(request)
    print jf

    country = {}
    if jf is 'json':
        country = {
            'CountryID': request.json['CountryID'],
            'CountryName': "'{0}'".format(request.json['CountryName'])
        }
    elif jf is 'form':
        country = {
            'CountryID': request.form['CountryID'],
            'CountryName': request.form['CountryName']
        }
    else:
        abort(400)

    print country
    new_country = Country(country)
    return dao.create_row_in_country(new_country)

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

@app.route('/cities', methods=['POST'])
def create_city():
    #return request
    jf = json_or_form(request)
    print jf

    city = {}
    if jf is 'json':
        city = { 
            'CityID': request.json['CityID'],
            'CityName': "'{0}'".format(request.json['CityName']),
            'CountryID': request.json['CountryID']
        }
    elif jf is 'form':
        city = {
            'CityID': request.form['CityID'],
            'CityName': request.form['CityName'],
            'CountryID': request.form['CountryID']
        }
    else:
        abort(400)

    print city
    new_city = City(city)
    return dao.create_row_in_city(new_city)

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

@app.route('/addresses', methods=['POST'])
def create_address():
    #return request
    jf = json_or_form(request)
    print jf

    address = {}
    if jf is 'json':
        address = {
            'AddressID': request.json['AddressID'],
            'Address1': "'{0}'".format(request.json['Address1']),
            'Address2': "'{0}'".format(request.json['Address2']),
            'District': "'{0}'".format(request.json['District']),
            'CityID': request.json['CityID'],
            'PostalCode': request.json['PostalCode'],
            'CountryID': request.json['CountryID'],
        }
    elif jf is 'form':
        address = {
            'AddressID' :request.form['AddressID'],
            'Address1': request.form['Address1'],
            'Address2':request.form['Address2'],
            'District':request.form['District'],
            'CityID':request.form['CityID'],
            'PostalCode':request.form['PostalCode'],
            'CountryID': request.form['CountryID']
        }
    else:
        abort(400)

    print address
    new_address = Address(address)
    return dao.create_row_in_address(new_address)

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



@app.route('/customers', methods=['POST'])
def create_customer():
    #return request
    jf = json_or_form(request)
    print jf

    customer = {}
    if jf is 'json':
        customer = {
            'CustomerID': request.json['CustomerID'],
            'StoreID': request.json['StoreID'],
            'FirstName': "'{0}'".format(request.json['FirstName']),
            'LastName': "'{0}'".format(request.json['LastName']),
            'EmailID': "'{0}'".format(request.json['EmailID']),
            'AddressID': request.json['AddressID'],
            'Active': "'{0}'".format(request.json['Active']),
            'CreateDate': "'{0}'".format(request.json['CreateDate']),
            'LastUpdate': "'{0}'".format(request.json['LastUpdate'])
        }
    elif jf is 'form':
        customer = {
           'CustomerID': request.form['CustomerID'],
            'StoreID' : request.form['StoreID'],
            'FirstName' : request.form['FirstName'],
            'LastName' : request.form['LastName'],
            'EmailID' : request.form['EmailID'],
            'AddressID' : request.form['AddressID'],
            'Active' : request.form['Active'],
            'CreateDate' : request.form['CreateDate'],
            'LastUpdate' : request.form['LastUpdate']
        }
    else:
        abort(400)

    print customer
    new_customer = Customer(customer)
    return dao.create_row_in_customer(new_customer)

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


@app.route('/customers/q/<query>', methods=['GET'])
def query_customer(query):
    query_dict, and_query = parse_query(query, Customer.field_to_database_column())
    customers = dao.query_customers(query_dict, and_query)
    return get_right_format(customers, request)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
