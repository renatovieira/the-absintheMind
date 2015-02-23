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
        test = "INSERT INTO COUNTRY (CountryID, CountryName) VALUES (CountryID={0},CountryName={1})".format(country['CountryID'],country['CountryName'])
        print test
        self.cursor.execute("INSERT INTO COUNTRY (CountryID, CountryName) VALUES (CountryID={0},CountryName={1})".format(country['CountryID'],country['CountryName']))
        self.cursor.connection.commit()
        return "/countries/{0}".format(country['CountryID'])

    def create_row_in_city(self,request):
        city = {
                'CityID': request.form['CityID'],
                'CityName': request.form['CityName'],
                'CountryID': request.form['CountryID']
        }

        self.cursor.execute("INSERT INTO CITY (CityID, CityName, CountryID) VALUES (CityID={0},CityName={1},CountryID={2})".format(city['CityID'],city['CityName'], city['CountryID']))
        self.cursor.connection.commit()

        return "/cities/{0}".format(city['CityID'])

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
        self.cursor.execute("INSERT INTO ADDRESS (AddressID, Address1, Address2, District, CityID, PostalCode, CountryID)"
                            " VALUES ({0},{1},{2},{3},{4},{5},{6})"
                            .format(address['AddressID'],address['Address1'],address['Address2'],address['District'],
                                    address['CityID'],address['PostalCode'],address['CountryID']))
        self.cursor.connection.commit()
        return "/addresses/{0}".format(address['AddressID'])

    def create_row_in_customer(self,request):
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

        self.cursor.execute("INSERT INTO CUSTOMER (CustomerID, StoreID, FirstName, LastName, EmailID, AddressID, Active, CreateDate, LastUpdate) VALUES (CustomerID={0},StoreID={1},FirstName={2},LastName={3},EmailID={4},AddressID={5},Active={6}, CreateDate={7},LastUpdate={8})".format(customer['CustomerID'],customer['StoreID'],customer['FirstName'],customer['LastName'],customer['EmailID'],customer['AddressID'],customer['Active'],customer['CreateDate'],customer['LastUpdate']))
        self.cursor.connection.commit()
        return "/customers/{0}".format(customer['CustomerID'])

    #Update methods
    def update_country(self, country):
        self.cursor.execute("UPDATE COUNTRY SET CountryName='{0}' WHERE CountryID={1}".format(country.name, country.id))

    def update_city(self, city):
        self.cursor.execute("UPDATE CITY SET CityName='{0}', CountryID={1} WHERE CityID={2}".format(city.name, city.country_id, city.id))

    def update_address(self, address):
        self.cursor.execute("UPDATE ADDRESS SET Address1='{0}', Address2='{1}', District='{2}', PostalCode={3}, CityID={4},"
                            " CountryID={5} WHERE AddressID={6}".format(address.address1, address.address2, address.district,
                                                                        address.postal_code, address.city_id, address.country_id, address.id))

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
    def find_x_by_y_dict(self, x, y_dict):
        print y_dict
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
                    query = "SELECT * FROM {0}'".format(x)
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
