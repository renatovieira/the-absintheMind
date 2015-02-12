from conf import *
import pymysql
from pymysql import IntegrityError


class Dao:
    def __init__(self):
        self.cursor = self.conn_db()

    def conn_db(self):
        host, user, password, database = read_db_conf()

        conn = pymysql.connect(host=host, user=user, passwd=password, db=database)
        return conn.cursor()

    def close_db(self):
        self.cursor.connection.close()
        self.cursor.close()

    #Get methods

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