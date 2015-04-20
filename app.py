#!flask/bin/python
from flask import Flask, request, abort, jsonify, render_template
from pymysql import IntegrityError
import pymysql
import pdb
from dao import Dao
from country import Country
from city import City
from address import Address
from customer import Customer
from page_obj import Page
from utils import *
from os import environ
import re

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

dao = Dao()

#Country
@app.route('/combined', methods=['POST'])
def create_city_country():
    #process the request data
    jf = json_or_form(request)
    city = {}
    if jf is 'json':
        c_name = request.json['CountryName']
        #ideally the user shouldn't need to set an id when creating a row. This try catch statement takes care of this scenario so now one can create a city and country just with names alone
        try:
            city = {
                'CityID': request.json['CityID'],
            }
        except KeyError:
            city = {
                'CityID': -1
            }
        city['CityName'] =  "'{0}'".format(request.json['CityName'])
    elif jf is 'form':
        c_name = request.form['CountryName']
        try:
            city = {
                'CityID': request.form['CityID'],
            }
        except KeyError:
            city = {
                'CityID': -1
            }
        city['CityName'] =  request.form['CityName']
    else:
        abort(400)

    # find out the country id
    temp_country = dao.find_country_by_name(c_name)
    if not temp_country:
        # by setting CountryID to -1, a dummy value, create_row_in_country will run the autoincrement version of insert
        new_country_data = {
            'CountryID': -1,
            'CountryName': "'{0}'".format(c_name)
        }

        new_country = Country(new_country_data)
        new_uri = dao.create_row_in_country(new_country)
        #temp solution because of what create_row returns right now (uri string with the id)
        city['CountryID'] = int(new_uri[(new_uri.rfind('/')+1):])
    else:
        city['CountryID'] = temp_country.id

    #make a new city with the country id field now
    new_city = City(city)
    return dao.create_row_in_city(new_city)

@app.route('/countries', methods=['GET'])
@app.route('/countries/page/<int:page_num>', methods=['GET'])
@app.route('/countries&fields="<string:fields>"', methods=['GET'])
@app.route('/countries/page/<int:page_num>&fields="<string:fields>"', methods=['GET'])
def get_countries(page_num=1, fields=None):
    query = request.query_string
    if query is None or len(query) == 0:
        countries = dao.get_countries(fields)
        pages = paginate(countries, 3, 'countries/page')
    else:
        query_dict = parse_query(query, Country.field_to_database_column())
        countries = dao.query_countries(query_dict, fields)
        pages = paginate(countries, 3, 'countries/page', '?q="{0}"'.format(query))
    try:
        print pages
        #print get_right_format(countries, request, dao, pages[page_num-1])
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
    except IndexError:
        abort(404)

@app.route('/countries/<int:country_id>', methods=['GET'])
@app.route('/countries/<int:country_id>&fields="<string:fields>"', methods=['GET'])
def find_country_by_id_projection(country_id, fields=None):
    return get_right_format([dao.find_country_by_id(country_id, fields)], request, dao)

@app.route('/countries', methods=['POST'])
def create_country():
    #return request
    jf = json_or_form(request)

    country = {}
    if jf is 'json':
        country = {
            'CountryID': request.json['CountryID'],
            'CountryName': "'{0}'".format(request.json['CountryName'])
        }
    elif jf is 'form':
        country = {
            'CountryID': request.form['CountryID'],
            'CountryName': "'{0}'".format(request.form['CountryName'])
        }
    else:
        abort(400)

    print country
    new_country = Country(country)
    dao.create_row_in_country(new_country)
    return jsonify({'country': new_country.serialize(dao)})

@app.route('/countries/<int:country_id>', methods=['DELETE'])
def del_country_by_id(country_id):
    temp = dao.delete_country_by_id(country_id)
    if not temp:
        abort(404)
    else:
        return get_countries()

@app.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    country = dao.find_country_by_id(country_id)
    if not request.json:
        dictionary = request.form
    else:
        dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    country.name = dictionary.get('CountryName', country.name)
    #update on the db
    dao.update_country(country)
    #return updated object
    return jsonify({'country': country.serialize(dao)})

#City
@app.route('/cities', methods=['GET'])
@app.route('/cities/page/<int:page_num>', methods=['GET'])
@app.route('/cities&fields="<string:fields>"', methods=['GET'])
@app.route('/cities/page/<int:page_num>&fields="<string:fields>"', methods=['GET'])
def get_cities(page_num=1, fields=None):
    query = request.query_string
    if query is None or len(query) == 0:
        cities = dao.get_cities(fields)
        pages = paginate(cities, 3, 'cities/page')
    else:
        query_dict = parse_query(query, City.field_to_database_column())
        cities = dao.query_cities(query_dict, fields)
        pages = paginate(cities, 3, 'cities/page', '?q="{0}"'.format(query))
    try:
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
    except IndexError:
        abort(404)

@app.route('/cities/<int:city_id>', methods=['GET'])
@app.route('/cities/<int:city_id>&fields="<string:fields>"', methods=['GET'])
def find_city_by_id(city_id, fields=None):
    return get_right_format([dao.find_city_by_id(city_id, fields)], request, dao)

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
            'CityName': "'{0}'".format(request.form['CityName']),
            'CountryID': request.form['CountryID']
        }
    else:
        abort(400)

    print city
    new_city = City(city)
    dao.create_row_in_city(new_city)
    return jsonify({'city': new_city.serialize(dao)})


@app.route('/cities/country/<int:country_id>', methods=['GET'])
@app.route('/cities/country/<int:country_id>/page', methods=['GET'])
@app.route('/cities/country/<int:country_id>/page/<int:page_num>', methods=['GET'])
def get_cities_by_country(country_id, page_num=1):
    cities = dao.find_cities_by_country_id(country_id)
    pages = paginate(cities, 1, 'cities/page')
    try:
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    temp = dao.delete_city_by_id(city_id)
    if not temp:
        abort(404)
    else:
        return get_cities()

@app.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    city = dao.find_city_by_id(city_id)
    if not request.json:
        dictionary = request.form
    else:
        dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    city.name = dictionary.get('CityName', city.name)
    city.country_id = dictionary.get('CountryID', city.country_id)
    #update on the db
    dao.update_city(city)
    #return updated object
    return jsonify({'city': city.serialize(dao)})

#Address
@app.route('/addresses', methods=['GET'])
@app.route('/addresses/page/<int:page_num>', methods=['GET'])
@app.route('/addresses&fields="<string:fields>"', methods=['GET'])
@app.route('/addresses/page/<int:page_num>&fields="<string:fields>"', methods=['GET'])
def get_addresses(page_num=1, fields=None):
    query = request.query_string
    if query is None or len(query) == 0:
        addresses = dao.get_addresses(fields)
        pages = paginate(addresses, 3, 'addresses/page')
    else:
        query_dict = parse_query(query, Address.field_to_database_column())
        addresses = dao.query_addresses(query_dict, fields)
        pages = paginate(addresses, 3, 'addresses/page', '?q="{0}"'.format(query))
    try:
#        return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/addresses/country/<int:country_id>', methods=['GET'])
@app.route('/addresses/country/<int:country_id>/page', methods=['GET'])
@app.route('/addresses/country/<int:country_id>/page/<int:page_num>', methods=['GET'])
def get_addresses_by_country(country_id, page_num=1):
    addresses = dao.find_addresses_by_country(country_id)
    pages = paginate(addresses, 1, 'addresses/page')
    try:
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/addresses/city/<int:city_id>', methods=['GET'])
@app.route('/addresses/city/<int:city_id>/page', methods=['GET'])
@app.route('/addresses/city/<int:city_id>/page/<int:page_num>', methods=['GET'])
def get_addresses_by_city(city_id, page_num=1):
    addresses = dao.find_addresses_by_city(city_id)
    pages = paginate(addresses, 1, 'addresses/page')
    try:
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/addresses/<int:address_id>', methods=['GET'])
@app.route('/addresses/<int:address_id>&fields="<string:fields>"', methods=['GET'])
def find_address_by_id_projection(address_id, fields=None):
    return get_right_format([dao.find_address_by_id(address_id, fields)], request, dao)

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
            'Address1': "'{0}'".format(request.form['Address1']),
            'Address2': "'{0}'".format(request.form['Address2']),
            'District': "'{0}'".format(request.form['District']),
            'CityID':request.form['CityID'],
            'PostalCode':request.form['PostalCode'],
            'CountryID': request.form['CountryID']
        }
    else:
        abort(400)

    print address
    new_address = Address(address)
    dao.create_row_in_address(new_address)
    return jsonify({'address': new_address.serialize(dao)})


@app.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    address = dao.find_address_by_id(address_id)
    if not request.json:
        dictionary = request.form
    else:
        dictionary = request.json
    #update all parameters that were sent, keep same information if a parameter has not been sent
    address.address1 = dictionary.get('Address1', address.address1)
    address.address2 = dictionary.get('Address2', address.address2)
    address.district = dictionary.get('District', address.district)
    address.postal_code = dictionary.get('PostalCode', address.postal_code)
    address.city_id = dictionary.get('CityID', address.city_id)
    address.country_id = dictionary.get('CountryID', address.country_id)
    #update on the db
    dao.update_address(address)
    #return updated object
    return jsonify({'address': address.serialize(dao)})



@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address_by_id(address_id):
    temp = dao.delete_address_by_id(address_id)
    if not temp:
        abort(404)
    else:
        return get_addresses()

#Customer
@app.route('/customers', methods=['GET'])
@app.route('/customers/page/<int:page_num>', methods=['GET'])
@app.route('/customers&fields="<string:fields>"', methods=['GET'])
@app.route('/customers/page/<int:page_num>&fields="<string:fields>"', methods=['GET'])
def get_customers(page_num=1, fields=None):
    query = request.query_string
    if query is None or len(query) == 0:
        customers = dao.get_customers(fields)
        pages = paginate(customers, 3, 'customers/page')
    else:
        query_dict = parse_query(query, Customer.field_to_database_column())
        customers = dao.query_customers(query_dict, fields)
        pages = paginate(customers, 3, 'customers/page', '?q="{0}"'.format(query))
    try:
#        return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/customers/country/<int:country_id>', methods=['GET'])
@app.route('/customers/country/<int:country_id>/page', methods=['GET'])
@app.route('/customers/country/<int:country_id>/page/<int:page_num>', methods=['GET'])
def get_customers_by_country(country_id, page_num=1):
    customers = dao.find_customers_by_country(country_id)
    pages = paginate(customers, 1, 'customers/page')
    try:
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/customers/city/<int:city_id>', methods=['GET'])
@app.route('/customers/city/<int:city_id>/page', methods=['GET'])
@app.route('/customers/city/<int:city_id>/page/<int:page_num>', methods=['GET'])
def get_customers_by_city(city_id, page_num=1):
    customers = dao.find_customers_by_city(city_id)
    pages = paginate(customers, 1, 'customers/page')
    try:
        #return render_template('basic_page.html', page=pages[page_num-1], result=get_right_format(pages[page_num-1].items, request, dao).get_data())
        return get_right_format(pages[page_num-1].items, request, dao, pages[page_num-1])
    except IndexError:
        abort(404)

@app.route('/customers/<int:customer_id>', methods=['GET'])
@app.route('/customers/<int:customer_id>&fields="<string:fields>"', methods=['GET'])
def find_customer_by_id_projection(customer_id, fields=None):
    return get_right_format([dao.find_customer_by_id(customer_id, fields)], request, dao)

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
            'FirstName': "'{0}'".format(request.form['FirstName']),
            'LastName': "'{0}'".format(request.form['LastName']),
            'EmailID': "'{0}'".format(request.form['EmailID']),
            'AddressID' : request.form['AddressID'],
            'Active': "'{0}'".format(request.form['Active']),
            'CreateDate': "'{0}'".format(request.form['CreateDate']),
            'LastUpdate': "'{0}'".format(request.form['LastUpdate'])
        }
    else:
        abort(400)

    print customer
    new_customer = Customer(customer)
    dao.create_row_in_customer(new_customer)
    return jsonify({'customer': new_customer.serialize(dao)})

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = dao.find_customer_by_id(customer_id)
    if not request.json:
        dictionary = request.form
    else:
        dictionary = request.json
    #update all parameters that were sent, keep information same if a parameter has not been sent
    customer.name.first = dictionary.get('FirstName', customer.name.first)
    customer.name.last = dictionary.get('LastName', customer.name.last)
    customer.email_id = dictionary.get('EmailID', customer.email_id)
    customer.store_id = dictionary.get('StoreID', customer.store_id)
    customer.address_id = dictionary.get('AddressID', customer.address_id)
    customer.active = dictionary.get('Active', customer.active)
    customer.create_date = dictionary.get('CreateDate', customer.create_date)
    #update on db
    dao.update_customer(customer)
    #return updated object
    return jsonify({'customer': customer.serialize(dao)})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    temp = dao.delete_customer_by_id(customer_id)
    if not temp:
        abort(404)
    else:
        return get_customers()

if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, processes=2)