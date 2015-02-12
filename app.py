#!flask/bin/python
from flask import Flask, jsonify
from country import Country
from city import City
from address import Address
from customer import Customer
from pymysql import IntegrityError
from conf import *
import pymysql
import pdb

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

countries = [
    Country(1, 'United States'), Country(2, 'Brazil'), Country(3, 'India')
]

cities = [
    City(1, 'New York', 1), City(2, 'Sao Paulo', 2), City(3, 'Bangalore', 3),
    City(4, 'Chicago', 1), City(5, 'San Francisco', 1)
]

addresses = [
    Address(1, '535 W 113th St.', 'Apartment 1', 'Manhattan', 10025, 1, 1),
    Address(2, '535 W 113th St.', 'Apartment 31', 'Manhattan', 10025, 1, 1),
    Address(3, 'Rua Francisco Lages, 117', '', 'Butanta', 05376150, 2, 2),
    Address(4, '230 North Michigan Avenue', '', 'Chicago', 60601, 4, 1)
]

customers = [
    Customer(1, 1, 'Renato', 'Nishimori', 1, 1, True, None),
    Customer(2, 2, 'Renato', 'Brazil', 3, 3, True, None)
]

#database configuration reading functions
host, user, password, database = read_db_conf()

#mysql cursors and pointers
# should modify this to match the specific database configuration you have
conn = pymysql.connect(host=host, user=user, passwd=password, db=database)
cur = conn.cursor()

#mysql functions
def conn_db():
    conn = pymysql.connect(host=host, user=user, passwd=passowrd, db=database)
    return conn.cursor()

def close_db(c):
    c.connection.close()
    c.close()

#Country

@app.route('/countries', methods=['GET'])
def get_countries():
    cur.execute("SELECT * FROM COUNTRY")
    return jsonify(countries=[country.serialize() for country in countries])

@app.route('/countries/<int:country_id>', methods=['DELETE'])
def del_country_by_id(country_id):
    return delete_x_by_y('COUNTRY','CountryID',country_id)

def find_country_by_id(country_id):
    for country in countries:
        if country.id == country_id:
            return country
    return None



#City

@app.route('/cities', methods=['GET'])
def get_cities():
    return jsonify(cities=[city.serialize() for city in cities])

@app.route('/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    return jsonify(cities=[city.serialize() for city in find_cities_by_country(country_id)])

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    return delete_x_by_y('CITY','CityID',city_id)

def find_city_by_id(city_id):
    for city in cities:
        if city.id == city_id:
            return city
    return None

def find_cities_by_country(country_id):
    filtered_cities = [city for city in cities if city.country_id==country_id]
    return filtered_cities

#Address

@app.route('/addresses', methods=['GET'])
def get_addresses():
    return jsonify(addresses=[address.serialize() for address in addresses])

@app.route('/addresses/country/<int:country_id>', methods=['GET'])
def get_addresses_by_country(country_id):
    return jsonify(addresses=[address.serialize() for address in find_addresses_by_country(country_id)])

@app.route('/addresses/city/<int:city_id>', methods=['GET'])
def get_addresses_by_city(city_id):
    return jsonify(addresses=[address.serialize() for address in find_addresses_by_city(city_id)])


def find_address_by_id(address_id):
    for address in addresses:
        if address.id == address_id:
            return address
    return None


def find_addresses_by_country(country_id):
    filtered_addresses = [address for address in addresses if address.country_id==country_id]
    return filtered_addresses


def find_addresses_by_city(city_id):
    filtered_addresses = [address for address in addresses if address.city_id==city_id]
    return filtered_addresses

#Customer

@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers=[customer.serialize() for customer in customers])

@app.route('/customers/country/<int:country_id>', methods=['GET'])
def get_customers_by_country(country_id):
    return jsonify(customers=[customer.serialize() for customer in find_customers_by_country(country_id)])

@app.route('/customers/city/<int:city_id>', methods=['GET'])
def get_customers_by_city(city_id):
    return jsonify(customers=[customer.serialize() for customer in find_customers_by_city(city_id)])

def find_customers_in_addresses(addresses):
    filtered_customers = []
    for customer in customers:
        for address in addresses:
            if customer.address_id == address.id:
                filtered_customers.append(customer)
                break
    return filtered_customers

def find_customers_by_country(country_id):
    filtered_addresses = find_addresses_by_country(country_id)
    return find_customers_in_addresses(filtered_addresses)

def find_customers_by_city(city_id):
    filtered_addresses = find_addresses_by_city(city_id)
    return find_customers_in_addresses(filtered_addresses)


#Delete method
def delete_x_by_y(x, y, y_val):
    try:
        cur.execute("SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val))
        temp = cur.fetchone()
        if temp == None:
            return "No {0} exists with given {1}: {2}".format(x,y,y_val)
        else:
            cur.execute("DELETE FROM {0} WHERE {1}={2}".format(x,y,y_val))
            conn.commit()
        return "deleted the following row: {0}".format(temp)
    except IntegrityError:
        return "Foreign key constraint failure"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
