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

# find x by name

    def find_country_by_name(self, country_name):
        self.find_x_by_y('COUNTRY', 'CountryName', "'{0}'".format(country_name))
        result = self.cursor.fetchone()
        if result is None:
            return False
        country = Country(result)
        return country

    def find_country_by_id(self, country_id):
        self.find_x_by_y('COUNTRY', 'CountryID', country_id)
        result = self.cursor.fetchone()
        if result is None:
            return "No countries found"
        country = Country(result)
        return country

    def find_city_by_id(self, city_id):
        self.find_x_by_y('CITY', 'CityID', city_id)
        result = self.cursor.fetchone()
        if result is None:
            return "No cities found"
        city = City(result)
        return city

    def find_address_by_id(self, address_id):
        self.find_x_by_y('ADDRESS', 'AddressID', address_id)
        result = self.cursor.fetchone()
        if result is None:
            return "No addresses found"
        address = Address(result)
        return address

    def find_customer_by_id(self, customer_id):
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
        print "SELECT * FROM {0} WHERE {1}={2}".format(x,y,y_val)
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
            return "deleted"
            #return "deleted the following row: {0}".format(temp)
        #except IntegrityError:
        #    return "Foreign key constraint failure"

    #Create methods

    def create_row_in_country(self,country):
        #print "INSERT INTO COUNTRY (CountryID, CountryName) VALUES ({0},{1})".format(country.id, country.name)
        if country.id is -1:
            print "auto incre country"
            self.cursor.execute("INSERT INTO COUNTRY (CountryName) VALUES ({0})".format(country.name))
            country.id = self.find_id_by_y('CountryID', 'COUNTRY', 'CountryName', country.name)
        else:
            self.cursor.execute("INSERT INTO COUNTRY (CountryID, CountryName) VALUES ({0},{1})".format(country.id, country.name))
        self.cursor.connection.commit()
        return "/countries/{0}".format(country.id)

    def create_row_in_city(self,city):
        if city.id is -1:
            print "auto incre city"
            self.cursor.execute("INSERT INTO CITY (CityName, CountryID) VALUES ({0},{1})".format(city.name, city.country_id))
            city.id = self.find_id_by_y('CityID', 'CITY', 'CityName', city.name)
        else:
            print "no incre city"
            print "INSERT INTO CITY (CityID, CityName, CountryID) VALUES ({0},{1},{2})".format(city.id, city.name, city.country_id)
            self.cursor.execute("INSERT INTO CITY (CityID, CityName, CountryID) VALUES ({0},{1},{2})".format(city.id, city.name, city.country_id))
        self.cursor.connection.commit()
        return "/cities/{0}".format(city.id)

    def create_row_in_address(self,address):
        if address.id is -1:
            self.cursor.execute("INSERT INTO ADDRESS (Address1, Address2, District, CityID, PostalCode, CountryID)"
                            " VALUES ({0},{1},{2},{3},{4},{5})"
                            .format(address.address1, address.address2, address.district,
                                    address.city_id, address.postal_code, address.country_id))
            address.id = self.find_id_by_y('AddressID', 'ADDRESS', 'AddressName', address.name)
        else:
            self.cursor.execute("INSERT INTO ADDRESS (AddressID, Address1, Address2, District, CityID, PostalCode, CountryID)"
                            " VALUES ({0},{1},{2},{3},{4},{5},{6})"
                            .format(address.id,address.address1, address.address2, address.district,
                                    address.city_id, address.postal_code, address.country_id))
        self.cursor.connection.commit()
        return "/addresses/{0}".format(address.id)

    #should be updated since we shouldn't be inputting createdate and lastupdate through the web app
    def create_row_in_customer(self,customer):
        if customer.id is -1:
            self.cursor.execute("INSERT INTO CUSTOMER (StoreID, FirstName, LastName, EmailID, AddressID, Active, CreateDate, LastUpdate) VALUES ({0},{1},{2},{3},{4},{5},{6},{7})".format(customer.store_id, customer.name.first, customer.name.last, customer.email_id, customer.address_id, customer.active, customer.create_date,customer.last_update))
            self.cursor.execute("SELECT CustomerID FROM CUSTOMER WHERE FirstName={0} AND LastName={1}".format(customer.name.first, customer.name.last))
            result = self.cursor.fetchone()
            customer.id = result['CustomerID']
        else:
            self.cursor.execute("INSERT INTO CUSTOMER (CustomerID, StoreID, FirstName, LastName, EmailID, AddressID, Active, CreateDate, LastUpdate) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8})".format(customer.id,customer.store_id, customer.name.first, customer.name.last, customer.email_id, customer.address_id, customer.active, customer.create_date,customer.last_update))
        self.cursor.connection.commit()
        return "/customers/{0}".format(customer.id)

    #Update methods
    def update_country(self, country):
        self.cursor.execute("UPDATE COUNTRY SET CountryName='{0}' WHERE CountryID={1}".format(country.name, country.id))

    def update_city(self, city):
        self.cursor.execute("UPDATE CITY SET CityName='{0}', CountryID={1} WHERE CityID={2}".format(city.name, city.country_id, city.id))

    def update_address(self, address):
        self.cursor.execute("UPDATE ADDRESS SET Address1='{0}', Address2='{1}', District='{2}', PostalCode={3}, CityID={4},"
                            " CountryID={5} WHERE AddressID={6}".format(address.Address1, address.Address2, address.District,
                                                                        address.PostalCode, address.CityID, address.CountryID, address.id))

    @staticmethod
    def field_to_database_column():
        return {'id': 'CustomerID', 'store_id': 'StoreID', 'first_name': 'FirstName',
                'last_name': 'LastName', 'email_id': 'EmailID', 'address_id': 'AddressID', 'active': 'Active'}

    def update_customer(self, customer):
        self.cursor.execute("UPDATE CUSTOMER SET FirstName='{0}', LastName='{1}', EmailID='{2}', "
                            "StoreID={3}, AddressID={4}, Active={5}, CreateDate='{6}' "
                            "WHERE CustomerID={7}".format(customer.name.first, customer.name.last, customer.email_id,
                                                          customer.store_id, customer.address_id, customer.active,
                                                          customer.create_date, customer.id))


    #Query methods
    def find_id_by_y(self, x, table, column, y):
        self.cursor.execute("SELECT {0} FROM {1} WHERE {2}={3}".format(x,table,column,y))
        result = self.cursor.fetchone()
        return result[x]

    def find_x_by_y_dict(self, x, y_dict):
        query = None
        for param in y_dict:
            if param[0] == '&':
                if query is None:
                    query = "SELECT * FROM {0} WHERE {1}='{2}'".format(x, param[1], param[2])
                else:
                    query = query + " AND {0}='{1}'".format(param[1], param[2])
            elif param[0] == '|':
                if query is None:
                    query = "SELECT * FROM {0} WHERE {1}='{2}'".format(x, param[1], param[2])
                else:
                    query = query + " OR {0}='{1}'".format(param[1], param[2])
            elif param[1] == 'LIMIT':
                if query is None:
                    query = "SELECT * FROM {0}".format(x)
                query = query + " LIMIT {0}".format(param[2])
            elif param[1] == 'OFFSET':
                query = query + " OFFSET {0}".format(param[2])

        print query
        self.cursor.execute(query)

    def query_countries(self, query_dict):
        self.find_x_by_y_dict('COUNTRY', query_dict)
        countries = []
        for row in self.cursor:
            countries.append(Country(row))
        return countries

    def query_cities(self, query_dict):
        self.find_x_by_y_dict('CITY', query_dict)
        cities = []
        for row in self.cursor:
            cities.append(City(row))
        return cities

    def query_addresses(self, query_dict):
        self.find_x_by_y_dict('ADDRESS', query_dict)
        addresses = []
        for row in self.cursor:
            addresses.append(Address(row))
        return addresses

    def query_customers(self, query_dict):
        self.find_x_by_y_dict('CUSTOMER', query_dict)
        customers = []
        for row in self.cursor:
            customers.append(Customer(row))
        return customers
