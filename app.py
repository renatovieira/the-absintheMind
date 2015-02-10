#!flask/bin/python
from flask import Flask, jsonify
from country import Country
from city import City
from address import Address
from costumer import Costumer

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

costumers = [
    Costumer(1, 1, 'Renato', 'Nishimori', 1, 1, True, None),
    Costumer(2, 2, 'Renato', 'Brazil', 3, 3, True, None)
]

#Country

@app.route('/countries', methods=['GET'])
def get_countries():
    return jsonify(countries=[country.serialize() for country in countries])

@app.route('/countries', methods=['POST'])
def post_countries():
    return jsonify(countries=[country.serialize() for country in countries])

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

#Costumer

@app.route('/costumers', methods=['GET'])
def get_costumers():
    return jsonify(costumers=[costumer.serialize() for costumer in costumers])

@app.route('/costumers/country/<int:country_id>', methods=['GET'])
def get_costumers_by_country(country_id):
    return jsonify(costumers=[costumer.serialize() for costumer in find_costumers_by_country(country_id)])

@app.route('/costumers/city/<int:city_id>', methods=['GET'])
def get_costumers_by_city(city_id):
    return jsonify(costumers=[costumer.serialize() for costumer in find_costumers_by_city(city_id)])

def find_costumers_in_addresses(addresses):
    filtered_costumers = []
    for costumer in costumers:
        for address in addresses:
            if costumer.address_id == address.id:
                filtered_costumers.append(costumer)
                break
    return filtered_costumers

def find_costumers_by_country(country_id):
    filtered_addresses = find_addresses_by_country(country_id)
    return find_costumers_in_addresses(filtered_addresses)

def find_costumers_by_city(city_id):
    filtered_addresses = find_addresses_by_city(city_id)
    return find_costumers_in_addresses(filtered_addresses)



if __name__ == "__main__":
    app.run(host="0.0.0.0")
