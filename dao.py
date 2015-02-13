from conf import *
import pymysql
from pymysql import IntegrityError
from country import Country
from city import City
from address import Address
from customer import Customer


class Dao:
    def __init__(self):
        self.cursor = self.conn_db()

    def conn_db(self):
        host, user, password, database = read_db_conf()

        conn = pymysql.connect(host=host, user=user, passwd=password, db=database)
        return conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.connection.close()
        self.cursor.close()

    #Get methods
    def get_x(self, x):
        self.cursor.execute("SELECT * FROM {0}".format(x))

    def get_countries(self):
        self.get_x('COUNTRY')
        countries = []
        for row in self.cursor:
            countries.append(Country(row))
        return countries

    def get_cities(self):
        self.get_x('CITY')
        cities = []
        for row in self.cursor:
            cities.append(City(row))
        return cities


    def get_addresses(self):
        self.get_x('ADDRESS')
        addresses = []
        for row in self.cursor:
            addresses.append(Address(row))
        return addresses

    def get_customers(self):
        self.get_x('CUSTOMER')
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers

    def find_country_by_id(self, country_id):
        result = self.find_x_by_y('COUNTRY', 'CountryID', country_id)
        if result == None:
            return "No countries found"
        return Country(result)

    def find_x_by_y(self, x, y, y_val):
        self.cursor.execute("SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val))
        temp = self.cursor.fetchone()
        return temp

    #Delete method
    def delete_country_by_id(self, country_id):
        return self.delete_x_by_y('COUNTRY', 'CountryID', country_id)

    def delete_city_by_id(self, city_id):
        return self.delete_x_by_y('CITY', 'CityID', city_id)

    def delete_address_by_id(self, address_id):
        return self.delete_x_by_y('ADDRESS', 'AddressID', address_id)

    def delete_customer_by_id(self, customer_id):
        return self.delete_x_by_y('CUSTOMER', 'CustomerID', customer_id)

    def delete_x_by_y(self, x, y, y_val):
        try:
            self.cursor.execute("SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val))
            temp = self.cursor.fetchone()
            if temp == None:
                return "No {0} exists with given {1}: {2}".format(x,y,y_val)
            else:
                self.cursor.execute("DELETE FROM {0} WHERE {1}={2}".format(x,y,y_val))
                self.cursor.conn.commit()
            return "deleted the following row: {0}".format(temp)
        except IntegrityError:
            return "Foreign key constraint failure"

    #Update methods
    def update_country(self, country):
        self.cursor.execute("UPDATE COUNTRY SET CountryName='{0}' WHERE CountryID={1}".format(country.name, country.id))

    def update_city(self, city):
	self.cursor.execute("UPDATE CITY SET CityName='{0}' WHERE CityID={1}".format(city.name, city.id))
