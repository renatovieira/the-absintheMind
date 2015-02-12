#!flask/bin/python
from flask import Flask, jsonify
from dao import Dao

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

def find_country_by_id(country_id):
    for country in countries:
        if country.id == country_id:
            return country
    return None

#City

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = dao.get_cities()
    return jsonify(cities=[city.serialize() for city in cities])

@app.route('/cities/country/<int:country_id>', methods=['GET'])
def get_cities_by_country(country_id):
    return jsonify(cities=[city.serialize() for city in find_cities_by_country(country_id)])

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    return dao.delete_city_by_id(city_id)

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
    addresses = dao.get_addresses()
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


@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address_by_id(address_id):
    return dao.delete_address_by_id(address_id)

def find_addresses_by_country(country_id):
    filtered_addresses = [address for address in addresses if address.country_id==country_id]
    return filtered_addresses


def find_addresses_by_city(city_id):
    filtered_addresses = [address for address in addresses if address.city_id==city_id]
    return filtered_addresses

#Customer

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = dao.get_customers()
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

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    return dao.delete_customer_by_id(customer_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
