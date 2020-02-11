import csv
import mysql.connector
from mysql.connector import Error


def create_dbtable():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", database="shopdb", password="")
        cursor = conn.cursor()
        query = """create table if not exists cities(id int(30) not null auto_increment primary key, city varchar(20), city_ascii varchar(20), lat varchar(20), lng varchar(10), country varchar(30), iso3 varchar(5), admin_name varchar(20), population varchar(20))"""
        cursor.execute(query)
        print("New database table created successfully")
    except Error as e:
        print("Can't perform the operation: {}".format(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def cronjob_insert():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", database="shopdb", password="")
        cursor = conn.cursor()

        info = csv.DictReader(open("D:\Python\Flask_Docker_Project\static\worldcities.csv", "r", errors='ignore'))
        
        #print(info)
        
        for data in info:
            row = dict(data)
            input_vals = (row["city"], row["city_ascii"], row["lat"], row["lng"], row["country"], row["iso3"], row["admin_name"], row["population"])
            print(input_vals)
            query = """ insert into cities(city, city_ascii, lat, lng, country, iso3, admin_name, population) values(%s, %s, %s, %s, %s, %s, %s, %s) """
            cursor.execute(query, input_vals)
        conn.commit()
        print("Data from csv file inserted into database successfully")

    except Error as e:
        print("Can't insert data into database: {}".format(e))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

create_dbtable()
cronjob_insert()
