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
            city = City(row)
            cities.append(city)
        return cities

    def get_addresses(self):
        self.get_x('ADDRESS')
        addresses = []
        for row in self.cursor:
            address = Address(row)
            addresses.append(address)
        return addresses

    def get_customers(self):
        self.get_x('CUSTOMER')
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers

    def find_country_by_id(self, country_id):
        self.find_x_by_y('COUNTRY', 'CountryID', country_id)
        result = self.cursor.fetchone()
        if result == None:
            return "No countries found"
	country = Country(result)
        return country

    def find_city_by_id(self, city_id):
        self.find_x_by_y('CITY', 'CityID', city_id)
        result = self.cursor.fetchone()
        if result == None:
            return "No cities found"
        city = City(result)
        city.country = self.find_country_by_id(city.country_id)
        return city

    def find_address_by_id(self, address_id):
	self.find_x_by_y('ADDRESS', 'AddressID', address_id)
	result = self.cursor.fetchone()
	if result == None:
		return "No addresses found"
	address = Address(result)
	address.city = self.find_addresses_by_city(address.city_id)
	address.country = self.find_addresses_by_country(address.country_id)
	return address

    def find_customer_by_id(self, custoemr_id):
	self.find_x_by_y('CUSTOMER', 'CustomerID', customer_id)
	result = self.cursor.fetchone()
	if result == None:
		return "No such customer"
	customer = Customer(result)
	return customer

    def find_cities_by_country_id(self, country_id):
        self.find_x_by_y('CITY', 'CountryID', country_id)
        cities = []
        for row in self.cursor:
            cities.append(City(row))
        return cities

    def find_addresses_by_country(self, country_id):
        self.find_x_by_y('ADDRESS', 'CountryID', country_id)
        addresses = []
        for row in self.cursor:
            addresses.append(Address(row))
        return addresses

    def find_addresses_by_city(self, city_id):
        self.find_x_by_y('ADDRESS', 'CityID', city_id)
        addresses = []
        for row in self.cursor:
            addresses.append(Address(row))
        return addresses

    def find_customers_by_country(self, country_id):
        self.cursor.execute("SELECT * FROM CUSTOMER WHERE AddressID IN "
                            "(SELECT AddressID from ADDRESS WHERE CountryID = {0})".format(country_id))
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers

    def find_customers_by_city(self, city_id):
        self.cursor.execute("SELECT * FROM CUSTOMER WHERE AddressID IN "
                            "(SELECT AddressID from ADDRESS WHERE CityID = {0})".format(city_id))
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers

    def find_x_by_y(self, x, y, y_val):
        self.cursor.execute("SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val))

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
        #try:
        self.cursor.execute("SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val))
        temp = self.cursor.fetchone()
        if temp == None:
            #abort(404)
            return False
            #return "No {0} exists with given {1}: {2}".format(x,y,y_val)
        else:
            self.cursor.execute("DELETE FROM {0} WHERE {1}={2}".format(x,y,y_val))
            self.cursor.connection.commit()
            return "deleted the following row: {0}".format(temp)
        #except IntegrityError:
        #    return "Foreign key constraint failure"

    #Create methods

    def create_row_in_country(self,request):
        country = {
            'CountryID': request.form['CountryID'],
            'CountryName': request.form['CountryName']
        }
        test = "INSERT INTO CITY (CountryID, CountryName) VALUES (CountryID={0},CountryName={1})".format(country['CountryID'],country['CountryName'])
        print test
        self.cursor.execute("INSERT INTO CITY (CountryID, CountryName) VALUES (CountryID={0},CountryName={1})".format(country['CountryID'],country['CountryName']))

    def create_row_in_address(self,request):
        address = {
            'AddressID' :request.form['AddressID'],
            'Address1': request.form['Address1'],
            'Address2':request.form['Address2'],
            'District':request.form['District'],
            'CityID':request.form['CityID'],
            'PostalCode':request.form['PostalCode'],
            'CountryID': request.form['CountryID']
        }
        print "INSERT INTO ADDRESS (AddressID, Address1, Address2, District, CityID, PostalCode, CountryID) VALUES (AddressID={0},Address1={1},Address2={2},District={3},CityID={4},PostalCode={5},CountryID={6})".format(address['AddressID'],address['Address1'],address['Address2'],address['District'],address['CityID'],address['PostalCode'],address['CountryID'])
        self.cursor.execute("INSERT INTO ADDRESS (AddressID, Address1, Address2, District, CityID, PostalCode, CountryID) VALUES ({0},{1},{2},{3},{4},{5},{6})".format(address['AddressID'],address['Address1'],address['Address2'],address['District'],address['CityID'],address['PostalCode'],address['CountryID']))
        self.cursor.connection.commit()


        #Update methods
    def update_country(self, country):
        self.cursor.execute("UPDATE COUNTRY SET CountryName='{0}' WHERE CountryID={1}".format(country.name, country.id))

    def update_city(self, city):
        self.cursor.execute("UPDATE CITY SET CityName='{0}', CountryID={1} WHERE CityID={2}".format(city.name, city.country_id, city.id))

    def update_address(self, address):
	self.cursor.execute("UPDATE ADDRESS SET Address1='{0}', Address2='{1}', District='{2}', PostalCode={3}, CityID={4}, CountryID={5} WHERE AddressID={6}".format(address.address1, address.address2, address.district, address.postalcode, address.city_id, address.country_id, address.id))

    def update_customer(self, customer):
	self.cursor.execute("UPDATE CUSTOMER SET FirstName='{0}', LastName='{1}', EmailID='{2}', StoreID={3}, AddressID={4}, Active={5}, CreateDate='{6}', LastUpdate='{7}' WHERE CustomerID={8}".format(customer.firstname, customer.lastname, customer.emailid, customer.store_id, customer.address_id, customer.active, customer.createdate, customer.lastupdate, customer.id))

    #Query methods
    def find_x_by_y_dict(self, x, y_dict, and_query):
        query = None
        for param in y_dict:
            if param[0] != 'OFFSET' and param[0] != 'LIMIT':
                if query is None:
                    query = "SELECT * FROM {0} WHERE {1}='{2}'".format(x, param[0], param[1])
                elif and_query:
                    query = query + " AND {0}='{1}'".format(param[0], param[1])
                else:
                    query = query + " OR {0}='{1}'".format(param[0], param[1])
        for param in y_dict:
            if param[0] == 'LIMIT':
                query = query + " LIMIT {0}".format(param[1])
            elif param[0] == 'OFFSET':
                query = query + " OFFSET {0}".format(param[1])
        print query
        self.cursor.execute(query)

    def query_countries(self, query_dict, and_query):
        self.find_x_by_y_dict('COUNTRY', query_dict, and_query)
        countries = []
        for row in self.cursor:
            countries.append(Country(row))
        return countries

    def query_cities(self, query_dict, and_query):
        self.find_x_by_y_dict('CITY', query_dict, and_query)
        cities = []
        for row in self.cursor:
            cities.append(City(row))
        return cities

    def query_addresses(self, query_dict, and_query):
        self.find_x_by_y_dict('ADDRESS', query_dict, and_query)
        addresses = []
        for row in self.cursor:
            addresses.append(Address(row))
        return addresses

    def query_customers(self, query_dict, and_query):
        self.find_x_by_y_dict('CUSTOMER', query_dict, and_query)
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers
